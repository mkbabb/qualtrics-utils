from enum import Enum


class GetSchemaResponseResultPropertiesDisplayedValuesAdditionalPropertiesType(
    str, Enum
):
    ARRAY = "array"

    def __str__(self) -> str:
        return str(self.value)
