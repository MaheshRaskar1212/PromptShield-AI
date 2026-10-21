
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_security_scan_returns_report():
    response = client.post(
        "/api/v1/security-tests/run",
        json={
            "target_id": "demo-chatbot",
            "categories": [
                "prompt_injection",
                "sensitive_data_leakage",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "completed"
    assert data["target_id"] == "demo-chatbot"
    assert data["total_tests"] == 4
    assert data["passed"] == 2
    assert data["failed"] == 2
    assert len(data["results"]) == 4


def test_reject_unknown_target():
    response = client.post(
        "/api/v1/security-tests/run",
        json={
            "target_id": "external-target",
            "categories": ["prompt_injection"],
        },
    )

    assert response.status_code == 422


def test_reject_unknown_category():
    response = client.post(
        "/api/v1/security-tests/run",
        json={
            "target_id": "demo-chatbot",
            "categories": ["unknown_test"],
        },
    )

    assert response.status_code == 422


def test_reject_empty_categories():
    response = client.post(
        "/api/v1/security-tests/run",
        json={
            "target_id": "demo-chatbot",
            "categories": [],
        },
    )

    assert response.status_code == 422


def test_reject_duplicate_categories():
    response = client.post(
        "/api/v1/security-tests/run",
        json={
            "target_id": "demo-chatbot",
            "categories": [
                "prompt_injection",
                "prompt_injection",
            ],
        },
    )

    assert response.status_code == 422


def test_cors_allows_configured_frontend_origin():
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )


def test_cors_rejects_unconfigured_frontend_origin():
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in response.headers


def test_reject_oversized_request_body():
    oversized_body = b"x" * (1_048_576 + 1)

    response = client.post(
        "/api/v1/security-tests/run",
        content=oversized_body,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "Request body too large."
