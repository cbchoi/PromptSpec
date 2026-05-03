"""Shared API error response helpers."""

from __future__ import annotations

from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict


class ErrorDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: dict[str, Any] = {}


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: ErrorDetail


async def value_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=ErrorDetail(code="VALIDATION_ERROR", message=str(exc), details={})
        ).model_dump(),
    )


def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            error=ErrorDetail(code=code, message=message, details={})
        ).model_dump(),
    )
