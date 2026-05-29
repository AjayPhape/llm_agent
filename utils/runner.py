import logging

from google.adk import Runner
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.adk.sessions import BaseSessionService
from google.genai.types import Content, Part

from schemas.generic import Response

logger = logging.getLogger("__name__")


async def run_agent(
    runner: Runner,
    session_service: BaseSessionService,
    app_name: str,
    user_id: str,
    session_id: str,
    message: str,
    state_keys: list[str] | None = None,
    initial_state: dict = None,
) -> Response:
    session_vars = {
        "session_id": session_id,
        "user_id": user_id,
        "app_name": app_name,
    }
    try:
        await session_service.create_session(**session_vars, state=initial_state or {})
    except AlreadyExistsError:
        logger.info("Fetching session already exists")
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
    state = {}
    if state_keys:
        for k in state_keys:
            if k in updated_session.state:
                state[k] = updated_session.state[k]
    resp = Response(
        statusCode=200,
        message=result,
        state=state,
        session_id=session_id,
    )
    logger.info(resp)
    return resp
