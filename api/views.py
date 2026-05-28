import logging
import uuid

from fastapi import APIRouter

from api.agent import run_agent
from api.schema import UserQuery

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat")
async def chat(req: UserQuery):
    user_id = req.userId
    message = req.message
    session_id = req.sessionId or str(uuid.uuid4())
    response = await run_agent(user_id, session_id, message)
    logger.info(response)

    return response
