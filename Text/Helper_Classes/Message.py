from .Tool_Call import Tool_Call
from typing import Literal

class Message:
    def __init__(self, content: str, role: Literal["user", "developer", "assistant", "tool"], tool_calls: list[Tool_Call] = [], tool_call_id = ""):
        if len(tool_calls) > 0 and content != None:
            raise ValueError("`content` must be None if `len(tool_calls)`>0")

        if not role in ["user", "developer", "assistant", "tool"]:
            raise ValueError(f"role must be either 'user', 'developer', 'assistant' or 'tool'. not: {role}")

        self.content = content
        self.role = role
        self.tool_calls = tool_calls
        self.tool_call_id = tool_call_id