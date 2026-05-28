import json
import logging

from google.adk import Agent, Runner
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.adk.errors.session_not_found_error import SessionNotFoundError
from google.adk.sessions import DatabaseSessionService
from google.genai.types import Content, Part

from api.prompts import PROMPT
from api.schema import OutputSchema
from api.tools import build_tools
from config import LLM_MODEL, LLM_URL
from config.db import DB_ENV
from custom_llm.llm_custom import LiteLlmCustom, agent_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = "to_do_list"

root_agent = Agent(
    name="todo_agent",
    model=agent_model,
    description="Todo Agent to assist user for todo list",
    instruction=PROMPT,
    tools=build_tools,
    output_schema=OutputSchema,
)

session_service = DatabaseSessionService(DB_ENV.db_url)
runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)


async def run_agent(user_id: str, session_id: str, message: str) -> dict:
    global runner
    session_vars = {
        "session_id": session_id,
        "user_id": user_id,
        "app_name": APP_NAME,
    }
    try:
        await session_service.create_session(**session_vars, state={"to_do_list": []})
    except AlreadyExistsError:
        pass

    new_msg = Content(
        role="user",
        parts=[Part(text=message)],
    )
    events = runner.run_async(
        user_id=user_id, session_id=session_id, new_message=new_msg
    )
    result = ""
    async for event in events:
        if event.is_final_response():
            result = event.content.parts[0].text or ""

    updated_session = await session_service.get_session(**session_vars)
    resp = {
        "message": result,
        "to_do_list": updated_session.state.get("to_do_list", []),
    }
    logger.info(resp)
    return resp
