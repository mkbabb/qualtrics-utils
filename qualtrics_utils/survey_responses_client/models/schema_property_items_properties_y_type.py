from enum import Enum


class SchemaPropertyItemsPropertiesYType(str, Enum):
    NUMBER = "number"

    def __str__(self) -> str:
        return str(self.value)
