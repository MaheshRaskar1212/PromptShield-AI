
from typing import Any

from app.services.demo_target import query_demo_chatbot
from app.services.detector import analyze_response
from app.services.test_cases import SECURITY_TEST_CASES


def run_security_scan(
    categories: list[str],
) -> dict[str, Any]:
    """Run selected security tests against the controlled demo chatbot."""

    results = []

    selected_cases = [
        test_case
        for test_case in SECURITY_TEST_CASES
        if test_case["category"] in categories
    ]

    for test_case in selected_cases:
        target_result = query_demo_chatbot(test_case["prompt"])

        analysis = analyze_response(
            test_case=test_case,
            target_result=target_result,
        )

        results.append(analysis)

    total = len(results)
    passed = sum(1 for result in results if result["passed"])
    failed = total - passed

    return {
        "target_id": "demo-chatbot",
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }
