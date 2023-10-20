from enum import Enum


class GetSchemaResponseResultPropertiesResponseIdType(str, Enum):
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
