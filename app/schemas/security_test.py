
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


TestCategory = Literal[
    "prompt_injection",
    "sensitive_data_leakage",
    "unsafe_output",
]


class SecurityTestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_id: Literal["demo-chatbot"] = "demo-chatbot"
    categories: list[TestCategory] = Field(
        min_length=1,
        max_length=3,
    )


class SecurityTestResponse(BaseModel):
    run_id: UUID
    status: Literal["accepted"]
    target_id: str
    categories: list[TestCategory]
    dry_run: bool = True
    message: str
