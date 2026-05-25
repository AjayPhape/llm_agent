from google.adk import Context, Event

from schemas.intent import IntentSchema


def router(node_input: IntentSchema, ctx: Context) -> Event:
    return Event(route=node_input.intent, message=node_input.userQuery)
