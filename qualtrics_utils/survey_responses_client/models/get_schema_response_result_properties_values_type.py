from enum import Enum


class GetSchemaResponseResultPropertiesValuesType(str, Enum):
    OBJECT = "object"

    def __str__(self) -> str:
        return str(self.value)
