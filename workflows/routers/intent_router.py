from google.adk import Context, Event

from schemas.intent import IntentSchema


def router(node_input: IntentSchema, ctx: Context) -> Event:
    ctx.state["intent"] = node_input.intent
    ctx.state["userQuery"] = node_input.userQuery
    return Event(route=node_input.intent, message=node_input.userQuery)
