from enum import Enum


class SchemaPropertyType(str, Enum):
    ARRAY = "array"
    INTEGER = "integer"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
