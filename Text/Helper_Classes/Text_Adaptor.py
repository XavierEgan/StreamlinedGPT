from ..Tool import Tool
from .Message import Message
import json
from typing import Literal

class Text_Adaptor:
    def __init__(self):
        pass

    def get_completion_with_history(self, message_history: list[Message], model: str, tools: list[Tool], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        pass

    def get_completion(self, message: str | None, model: str, tools: list[Tool] = [], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        pass

    def _get_tool_string(self, tool: Tool) -> str:
        pass