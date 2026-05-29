import logging

from google.adk import Agent

from custom_llm.llm_custom import agent_model

from .prompts import PROMPT
from .tools import build_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


root_agent = Agent(
    name="weather_service_agent",
    model=agent_model,
    description="Based on latitude and longitude returns weather of the city",
    instruction=PROMPT,
    tools=build_tools,
)
