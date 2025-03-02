from .Tool import Tool
from .Helper_Classes.Message import Message
from .Helper_Classes.Adaptor import Adaptor
from typing import Literal
import json

class Assistant:
    def __init__(self, adaptor: Adaptor):
        self.message_history: list[Message] = []
        self.tools: list[Tool] = []
        self.tool_log: list[callable] = []

        self.adaptor: Adaptor = adaptor
    
    def send_message(self, message: str, model: str | None = None, tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        """
        Returns the Message object
        message: the message to send to the model
        model: the llm model used. None means use the default model
        tool_choice: str 'none', 'auto' or 'required'
        """
        kwargs = {
            "message" : message,
            "model" : model,
            "tools" : self.tools,
            "tool_choice" : tool_choice
        }

        if model == None:
            del kwargs["model"]

        response = self.adaptor.get_completion_with_history(**kwargs)

        self.message_history.append(response)

        self._manage_tool

        return response

    
    def send_message_without_history(self, message: str, model: str | None = None, tool_choice: Literal["none", "auto", "required"] = "auto"):
        """
        message: the message to send to the model
        model: the llm model used. None means use the default model
        tool_choice: str 'none', 'auto' or 'required'
        """
        kwargs = {
            "message" : message,
            "model" : model,
            "tools" : self.tools,
            "tool_choice" : tool_choice
        }
        if model == None:
            del kwargs["model"]

        message_history = []

        response = self.adaptor.get_completion(**kwargs)

        message_history = [response] + self._manage_tool_no_history(response)

        response = self.adaptor.get_completion

        return response

    def _manage_tool(self, message: Message) -> None:
        if len(message.tool_calls) == 0:
            return # there were no tool calls
        
        for tool_call in message.tool_calls:
            try:
                tool_response = self.tool_log[tool_call.name](**json.loads(tool_call.arguments))
            except Exception as e:
                tool_response = f"Tool {tool_call.name} had the following error: '{e}'"
                print(f"Tool {tool_call.name} had the following error: '{e}'")
            
            self.message_history.append(
                Message(
                    content=tool_response,
                    role="tool",
                    tool_calls=[],
                    tool_call_id=tool_call.id
                )
            )
    
    def _manage_tool_no_history(self, message: Message) -> list[Message]:
        if len(message.tool_calls) == 0:
            return # there were no tool calls
        
        messages = []

        for tool_call in message.tool_calls:
            try:
                tool_response = self.tool_log[tool_call.name](**json.loads(tool_call.arguments))
            except Exception as e:
                tool_response = f"Tool {tool_call.name} had the following error: '{e}'"
                print(f"Tool {tool_call.name} had the following error: '{e}'")
            
            messages.append(
                Message(
                    content=tool_response,
                    role="tool",
                    tool_calls=[],
                    tool_call_id=tool_call.id
                )
            )
        return messages
    
    def add_tool(self, tool: Tool) -> None:
        self.tool_log[tool.name] = tool.function

        self.tools.append(tool)