from enum import Enum


class SchemaPropertyItemsPropertiesXType(str, Enum):
    NUMBER = "number"

    def __str__(self) -> str:
        return str(self.value)
