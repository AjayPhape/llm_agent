from google.adk import Workflow

from agents import datetime_context_agent, intent_agent, weather_service_agent
from schemas.intent import IntentType

from .routers import intent_router

root_agent = Workflow(
    name="datetime_weather_workflow",
    description=(
        "Classifies the user query and retrieves either"
        "the current datetime for a timezone or weather information for a city."
    ),
    edges=[
        ("START", intent_agent),
        (intent_agent, intent_router),
        (
            intent_router,
            {
                IntentType.DATETIME: datetime_context_agent,
                IntentType.WEATHER: weather_service_agent,
            },
        ),
    ],
)
