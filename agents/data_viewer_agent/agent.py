import logging

from google.adk import Agent

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom

from .prompts import PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = LiteLlmCustom(
    model=LLM_MODEL,
    api_base=LLM_URL,
)


root_agent = Agent(
    name="data_viewer_agent",
    model=model,
    description=("Display data in tabular format"),
    instruction=PROMPT,
    # tools=build_tools,
    # output_schema=List[str]
)
