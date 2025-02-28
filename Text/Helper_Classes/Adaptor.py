from Tool import Tool
from Text.Helper_Classes.Message import Message
import json
from typing import Literal

class Adaptor:
    def __init__(self):
        pass

    def get_completion_with_history(self, message_history: list[Message], model: str, tools: list[Tool], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        pass

    def get_completion(self, message: Message, model: str, tools: list[Tool]) -> Message:
        pass