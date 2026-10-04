from typing import Any

from pydantic import BaseModel, Field


# ==========================================
# ANALYSIS REQUEST
# ==========================================

class AnalyzeRequest(BaseModel):

    filename: str = Field(
        default="source.cpp",
        min_length=1,
        max_length=255
    )

    code: str = Field(
        ...,
        min_length=1
    )


# ==========================================
# ANALYSIS RESPONSE
# ==========================================

class AnalyzeResponse(BaseModel):

    success: bool

    filename: str

    syntax_errors: int

    basic_metrics: dict[str, Any]

    ast_metrics: dict[str, Any]

    complexity: dict[str, Any]

    risk: dict[str, Any]