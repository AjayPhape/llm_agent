from pydantic import BaseModel


class UserQuery(BaseModel):
    message: str
    userId: str
    sessionId: str | None = None


class OutputSchema:
    message: str
    to_do_list: list[dict]
