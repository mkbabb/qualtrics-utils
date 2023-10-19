from enum import Enum


class RequestStatus(str, Enum):
    COMPLETE = "complete"
    FAILED = "failed"
    INPROGRESS = "inProgress"

    def __str__(self) -> str:
        return str(self.value)
