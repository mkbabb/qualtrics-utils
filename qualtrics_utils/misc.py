from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

HEADERS = {"X-API-TOKEN": "", "Content-Type": "application/json"}

VERSION = "v3"

BASE_URL: Callable[
    [str], str
] = lambda x: f"https://yul1.qualtrics.com/API/{x}/surveys/"

T = TypeVar("T")


@dataclass
class ExportedFile(Generic[T]):
    surveyId: str
    fileId: str
    continuationToken: str
    data: T
