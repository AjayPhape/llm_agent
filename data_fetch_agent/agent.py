import logging

from google.adk import Agent

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom, agent_model

from .prompts import PROMPT
from .tools import build_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


root_agent = Agent(
    name="data_fetch_agent",
    model=agent_model,
    # description="Selects appropriate query based on user message and returns the result",
    instruction=PROMPT,
    tools=build_tools,
    # output_schema=List[str]
)
