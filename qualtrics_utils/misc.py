from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from datetime import datetime

HEADERS = {"X-API-TOKEN": "", "Content-Type": "application/json"}

VERSION = "v3"

BASE_URL: Callable[
    [str], str
] = lambda version: f"https://yul1.qualtrics.com/API/{version}/"

T = TypeVar("T")


@dataclass
class ExportedFile(Generic[T]):
    survey_id: str
    file_id: str

    continuation_token: str | None
    last_response_id: str | None

    timestamp: datetime

    data: T
