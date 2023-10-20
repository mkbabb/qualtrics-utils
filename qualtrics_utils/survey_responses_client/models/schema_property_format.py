from enum import Enum


class SchemaPropertyFormat(str, Enum):
    DATE_TIME = "date-time"

    def __str__(self) -> str:
        return str(self.value)
