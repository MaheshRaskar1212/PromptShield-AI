
from uuid import uuid4

from fastapi import APIRouter

from app.schemas.security_test import (
    SecurityTestRequest,
    SecurityTestResponse,
)
from app.services.security_engine import run_security_scan


router = APIRouter(prefix="/api/v1", tags=["Security Tests"])


@router.post(
    "/security-tests/run",
    response_model=SecurityTestResponse,
    status_code=200,
)
def run_security_test(
    request: SecurityTestRequest,
) -> SecurityTestResponse:
    report = run_security_scan(request.categories)

    return SecurityTestResponse(
        run_id=uuid4(),
        status="completed",
        **report,
    )
