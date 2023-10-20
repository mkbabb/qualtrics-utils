from enum import Enum


class GetSchemaResponseResultPropertiesLabelsType(str, Enum):
    OBJECT = "object"

    def __str__(self) -> str:
        return str(self.value)
