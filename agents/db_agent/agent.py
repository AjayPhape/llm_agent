import logging
from typing import List

from google.adk import Agent

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom

from .prompts import PROMPT
from .schemas import Data
from .tools import build_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = LiteLlmCustom(
    model=LLM_MODEL,
    api_base=LLM_URL,
)


root_agent = Agent(
    name="summerize_data_agent",
    model=model,
    description=(
        "Selects relevant columns from the user query to retrieve aggregated data."
    ),
    instruction=PROMPT,
    tools=build_tools,
    # output_schema=List[str]
)
