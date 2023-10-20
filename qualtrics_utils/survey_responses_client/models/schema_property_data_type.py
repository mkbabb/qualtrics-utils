from enum import Enum


class SchemaPropertyDataType(str, Enum):
    EMBEDDEDDATA = "embeddedData"
    METADATA = "metadata"
    QUESTION = "question"

    def __str__(self) -> str:
        return str(self.value)
