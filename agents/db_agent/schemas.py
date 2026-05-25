from pydantic.v1 import BaseModel, Field


class Data(BaseModel):
    columnName: str = Field(
        ...,
        description="database column name",
        min_length=1,
    )
