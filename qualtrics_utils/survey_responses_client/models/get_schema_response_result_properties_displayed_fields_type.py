from enum import Enum


class GetSchemaResponseResultPropertiesDisplayedFieldsType(str, Enum):
    ARRAY = "array"

    def __str__(self) -> str:
        return str(self.value)
