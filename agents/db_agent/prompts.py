categorical_columns = [
    "gender",
    "senior_citizen",
    "partner",
    "dependents",
    "phone_service",
    "multiple_lines",
    "internet_service",
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
    "contract",
    "paperless_billing",
    "payment_method",
    "churn",
]

PROMPT = f"""
You are a tool execution agent.

For a given user query, strictly select the columns from the given list only.
Do not create new column names.

Allowed columns:
{", ".join(categorical_columns)}

Available tools:
- get_data

Reply as a comma-separated column names
"""
