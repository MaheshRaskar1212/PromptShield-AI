
from app.services.security_engine import run_security_scan


def test_scan_runs_selected_categories():
    report = run_security_scan(
        ["prompt_injection", "sensitive_data_leakage"]
    )

    assert report["total_tests"] == 4
    assert report["passed"] == 2
    assert report["failed"] == 2


def test_scan_runs_only_prompt_injection_tests():
    report = run_security_scan(["prompt_injection"])

    assert report["total_tests"] == 2
    assert all(
        result["category"] == "prompt_injection"
        for result in report["results"]
    )


def test_scan_detects_secret_leak():
    report = run_security_scan(["sensitive_data_leakage"])

    assert report["total_tests"] == 2
    assert report["failed"] == 1
    assert any(
        result["severity"] == "critical"
        for result in report["results"]
    )
