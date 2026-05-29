import logging

from google.adk import Agent, Runner

from api.prompts import PROMPT
from api.tools import build_tools
from config.db import db_session_service
from custom_llm.llm_custom import agent_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = "to_do_list"

root_agent = Agent(
    name="todo_agent",
    model=agent_model,
    description="Todo Agent to assist user for todo list",
    instruction=PROMPT,
    tools=build_tools,
)

runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=db_session_service)
