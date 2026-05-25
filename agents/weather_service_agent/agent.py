import logging

from google.adk import Agent

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom

from .prompts import PROMPT
from .tools import build_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = LiteLlmCustom(
    model=LLM_MODEL,
    api_base=LLM_URL,
)


root_agent = Agent(
    name="weather_service_agent",
    model=model,
    description="Based on latitude and longitude returns weather of the city",
    instruction=PROMPT,
    tools=build_tools,
)
