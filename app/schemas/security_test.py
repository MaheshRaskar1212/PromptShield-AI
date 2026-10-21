
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


TestCategory = Literal[
    "prompt_injection",
    "sensitive_data_leakage",
    "unsafe_output",
]


class SecurityTestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_id: Literal["demo-chatbot"] = "demo-chatbot"
    categories: list[TestCategory] = Field(min_length=1, max_length=3)

    @field_validator("categories")
    @classmethod
    def categories_must_be_unique(
        cls,
        categories: list[TestCategory],
    ) -> list[TestCategory]:
        if len(categories) != len(set(categories)):
            raise ValueError("Duplicate security test categories are not allowed.")
        return categories


class SecurityFinding(BaseModel):
    test_id: str
    category: str
    passed: bool
    severity: str
    finding: str
    evidence: str | None = None
    remediation: str | None = None


class SecurityTestResponse(BaseModel):
    run_id: UUID
    status: Literal["completed"]
    target_id: str
    total_tests: int
    passed: int
    failed: int
    results: list[SecurityFinding]
