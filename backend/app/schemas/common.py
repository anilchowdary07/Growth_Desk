from __future__ import annotations

"""Common Pydantic schemas."""

from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int = 1
    page_size: int = 50


class StatusResponse(BaseModel):
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    detail: str
