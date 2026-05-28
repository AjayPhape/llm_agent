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

For the user query:
- Select columns only from the allowed list.
- Never generate or assume new column names.
- Use `get_column_list` only

Allowed columns:
{", ".join(categorical_columns)}

Return only valid JSON in this format:
{{
  "groupColumns": "comma-separated column names for grouping",
  "sortColumns": "comma-separated column names for sorting"
}}
"""
