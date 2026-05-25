from enum import Enum

from pydantic import BaseModel, Field


class IntentType(str, Enum):
    DATETIME = "DATETIME"
    WEATHER = "WEATHER"
    INVALID = "INVALID"


class IntentSchema(BaseModel):
    """
    Schema representing a classified user intent.
    """

    userQuery: str = Field(
        ...,
        description="Original query provided by the user.",
        min_length=1,
        examples=["What's the weather in Dublin?"],
    )

    intent: IntentType = Field(
        ...,
        description="Detected intent category for the user query.",
        examples=["WEATHER"],
    )
