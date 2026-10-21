
from starlette.responses import JSONResponse


MAX_REQUEST_BODY_BYTES = 1_048_576


class RequestBodyTooLarge(Exception):
    """Raised when an incoming request exceeds the configured limit."""


class RequestSizeLimitMiddleware:
    """Limit incoming HTTP request bodies to 1 MiB."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        content_length = next(
            (
                value.decode("latin-1")
                for name, value in scope["headers"]
                if name.lower() == b"content-length"
            ),
            None,
        )

        if content_length is not None:
            try:
                declared_length = int(content_length)
            except ValueError:
                await JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid Content-Length header."},
                )(scope, receive, send)
                return

            if declared_length < 0:
                await JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid Content-Length header."},
                )(scope, receive, send)
                return

            if declared_length > MAX_REQUEST_BODY_BYTES:
                await JSONResponse(
                    status_code=413,
                    content={"detail": "Request body too large."},
                )(scope, receive, send)
                return

        received_bytes = 0

        async def limited_receive():
            nonlocal received_bytes

            message = await receive()

            if message["type"] == "http.request":
                received_bytes += len(message.get("body", b""))

                if received_bytes > MAX_REQUEST_BODY_BYTES:
                    raise RequestBodyTooLarge

            return message

        response_started = False

        async def tracked_send(message):
            nonlocal response_started

            if message["type"] == "http.response.start":
                response_started = True

            await send(message)

        try:
            await self.app(scope, limited_receive, tracked_send)
        except RequestBodyTooLarge:
            if response_started:
                # The response has already started; it cannot be replaced.
                raise

            await JSONResponse(
                status_code=413,
                content={"detail": "Request body too large."},
            )(scope, receive, send)
