from datetime import datetime
from zoneinfo import ZoneInfo

from google.adk import Agent
from tzlocal.windows_tz import win_tz

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom


def get_datetime(tz) -> dict:
    """
    Returns a datetime in string format.
    :param tz:
    :return: dictionary with timezone information and current datetime as per timezone
    """
    return {
        "currentDateTime": datetime.now(tz=ZoneInfo(tz)).strftime("%y-%m-%d %H-%M-%S"),
        "timeZone": tz,
    }


mdl = LiteLlmCustom(
    model=LLM_MODEL,
    api_base=LLM_URL,
)

root_agent = Agent(
    name="tool_agent",
    model=mdl,
    description="Tool Agent",
    instruction=f"""
You are a tool execution engine.
For a given user query select appropriate IANA timezone,
Do not create a new timezone

Strictly select timezone from following list

{", ".join(win_tz.values())}

Available tools:
- get_current_datetime

Reply in natural language
    """,
    tools=[get_datetime],
)
