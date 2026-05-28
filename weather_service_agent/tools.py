import logging
from typing import Callable, Dict

import requests

logger = logging.getLogger(__name__)


def get_weather(lat: str, lon: str) -> Dict:
    """
    Retrieve weather data for a geographic location.

    Args:
        lat: Latitude of the location as a string.
        lon: Longitude of the location as a string.

    Returns:
        A dictionary containing weather information for the specified
        coordinates.
    """

    params = {
        "latitude": lat,
        "longitude": lon,
        "units": "Celsius",
        "current": ",".join(["temperature_2m"]),
    }
    try:
        response = requests.get(
            "http://api.open-meteo.com/v1/forecast",
            params=params,
        )
        json_response = response.json()
        logger.info(json_response)

    except requests.exceptions.RequestException as e:
        logger.exception(e)
        json_response = {
            "statusCode": 500,
            "statusMessage": str(e),
        }
    return json_response


build_tools: list[Callable] = [get_weather]
