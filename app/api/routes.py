
from uuid import uuid4

from fastapi import APIRouter

from app.schemas.security_test import (
    SecurityTestRequest,
    SecurityTestResponse,
)

router = APIRouter(prefix="/api/v1", tags=["Security Tests"])


@router.post(
    "/security-tests/run",
    response_model=SecurityTestResponse,
    status_code=202,
)
def run_security_test(
    request: SecurityTestRequest,
) -> SecurityTestResponse:
    return SecurityTestResponse(
        run_id=uuid4(),
        status="accepted",
        target_id=request.target_id,
        categories=request.categories,
        dry_run=True,
        message=(
            "Request validated. Execution is not implemented yet; "
            "this is a dry run."
        ),
    )
