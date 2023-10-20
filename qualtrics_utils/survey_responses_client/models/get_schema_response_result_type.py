from enum import Enum


class GetSchemaResponseResultType(str, Enum):
    OBJECT = "object"

    def __str__(self) -> str:
        return str(self.value)
