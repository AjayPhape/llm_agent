from typing import Any, Dict

from google.adk.models import LiteLlm

from config import LLM_MODEL, LLM_URL


class LiteLlmCustom(LiteLlm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        return {"model": self.model, "type": "LiteLlm (Web Safe Workaround)"}


agent_model = LiteLlmCustom(
    model=LLM_MODEL,
    api_base=LLM_URL,
)
