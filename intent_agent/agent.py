import logging

from google.adk import Agent

from config import LLM_MODEL, LLM_URL
from custom_llm.llm_custom import LiteLlmCustom, agent_model
from schemas.intent import IntentSchema

from .prompts import PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

root_agent = Agent(
    name="intent_agent",
    model=agent_model,
    description="Agent classify user message to intent",
    instruction=PROMPT,
    output_schema=IntentSchema,
)
