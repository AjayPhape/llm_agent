import logging
import uuid

from fastapi import APIRouter

from api.agent import APP_NAME, runner
from api.schema import UserQuery
from config.db import db_session_service
from schemas.generic import Response
from utils.runner import run_agent
from workflows.agent import APP_NAME as workflow_name
from workflows.agent import workflow_runner

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat")
async def chat(req: UserQuery) -> Response:
    user_id = req.userId
    message = req.message
    session_id = req.sessionId or str(uuid.uuid4())

    response = await run_agent(
        runner=runner,
        session_service=db_session_service,
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        message=message,
        state_keys=["to_do_list"],
        initial_state={"to_do_list": []},
    )

    return response


@router.post("/chat_workflow")
async def chat_workflow(req: UserQuery) -> Response:
    user_id = req.userId
    message = req.message
    session_id = req.sessionId or str(uuid.uuid4())

    response = await run_agent(
        runner=workflow_runner,
        session_service=db_session_service,
        app_name=workflow_name,
        user_id=user_id,
        session_id=session_id,
        message=message,
        state_keys=["InitialUserQuery", "intent", "userQuery"],
        initial_state={"InitialUserQuery": message},
    )

    return response
