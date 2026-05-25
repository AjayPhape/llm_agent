from pydantic import BaseModel


class TimeZone(BaseModel):
    """Timezone should be valid timezone"""

    timezone: str
