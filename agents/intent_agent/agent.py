import logging

from google.adk import Agent

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom
from schemas.intent import IntentSchema

from .prompts import PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = LiteLlmCustom(
    model=LLM_MODEL,
    api_base=LLM_URL,
)


root_agent = Agent(
    name="intent_agent",
    model=model,
    description="Agent classify user message to intent",
    instruction=PROMPT,
    output_schema=IntentSchema,
)
