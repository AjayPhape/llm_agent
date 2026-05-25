import logging

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom
from google.adk import Agent

from .prompts import PROMPT
from .tools import build_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = LiteLlmCustom(
    model=LLM_MODEL,
    api_base=LLM_URL,
)

root_agent = Agent(
    name="datetime_context_agent",
    model=model,
    description="Extract timezone from user query and returns current datetime for that timezone",
    instruction=PROMPT,
    tools=build_tools,
)
