import logging

from google.adk import Agent

from custom_llm.llm_custom import agent_model

# from schemas.db import HelperData
from .prompts import PROMPT
from .tools import build_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

root_agent = Agent(
    name="data_extractor_agent",
    model=agent_model,
    description=(
        "Selects relevant columns from the user query to retrieve aggregated data."
    ),
    instruction=PROMPT,
    tools=build_tools,
    # output_schema=HelperData
)
