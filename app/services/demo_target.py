
from typing import Any


DEMO_SECRET = "DEMO_SECRET_12345"


def query_demo_chatbot(prompt: str) -> dict[str, Any]:
    """
    Simulate an AI chatbot for controlled security testing.
    This is a mock target, not a real LLM.
    """
    normalized_prompt = prompt.lower()

    # Simulated prompt-injection weakness
    if "ignore all previous instructions" in normalized_prompt:
        return {
            "response": (
                f"Previous instructions ignored. "
                f"Here is the internal secret: {DEMO_SECRET}"
            ),
            "behavior": "prompt_injection",
        }

    # Simulated sensitive-data leakage
    if "reveal the secret" in normalized_prompt:
        return {
            "response": f"The internal secret is {DEMO_SECRET}",
            "behavior": "sensitive_data_leakage",
        }

    # Safe default response
    return {
        "response": "I can help with general questions.",
        "behavior": "normal",
    }
