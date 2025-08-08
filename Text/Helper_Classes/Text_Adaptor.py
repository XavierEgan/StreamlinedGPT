from ..Tool import Tool
from .Message import Message
from ..Common_Imports import *

class Text_Adaptor:
    def __init__(self):
        pass
    
    @abstractmethod
    def get_completion_with_history(self, message_history: list[Message], model: str, tools: list[Tool], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        pass

    @abstractmethod
    def get_completion(self, message: str | None, model: str, tools: list[Tool] = [], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        pass
    
    @abstractmethod
    def _get_tool_string(self, tool: Tool) -> dict[str, Any]:
        pass