import logging
from datetime import datetime
from typing import Callable, Dict
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def get_current_datetime(tz: str) -> Dict:
    """
    Retrieve the current date and time for a given timezone.

    Args:
        tz: Timezone identifier as a string (e.g. "Europe/Dublin").

    Returns:
        A dictionary containing the timezone and the current datetime
        formatted as a string for the specified timezone.
    """
    logger.info(f"Getting current datetime for {tz}")
    try:
        tz_obj = ZoneInfo(tz)

        return {
            "timezone": tz,
            "current_datetime": datetime.now(tz=tz_obj).strftime("%Y-%m-%d %H:%M:%S"),
        }

    except ValueError as e:
        logger.exception(e)
        return {"statusCode": 500, "statusMessage": str(e)}


build_tools: list[Callable] = [
    get_current_datetime,
]
