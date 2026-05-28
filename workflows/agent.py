from google.adk import Workflow

from agents import (
    data_fetch_agent,
    datetime_context_agent,
    db_agent,
    intent_agent,
    weather_service_agent,
)
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

# root_agent = Workflow(
#     name="summarised_data_agent",
#     description="Retrieves customer summarized data in tabular format",
#     edges=[
#         ("START", data_fetch_agent),
#         # (db_agent, data_fetch_agent),
#     ],
# )
