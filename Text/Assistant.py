from .Tool import Tool
from .Helper_Classes.Message import Message
from .Helper_Classes.Text_Adaptor import Text_Adaptor
from typing import Literal
import json

class Assistant:
    def __init__(self, adaptor: Text_Adaptor):
        self.message_history: list[Message] = []
        self.tools: list[Tool] = []
        self.tool_log: list[str : callable] = {}

        self.adaptor: Text_Adaptor = adaptor
    
    def send_message(self, message: str, model: str | None = None, tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        """
        Returns a Message object. Message.content to retrieve what the model said\n
        message: the message to send to the model\n
        model: the llm model used. None means use the default model\n
        tool_choice: str 'none', 'auto' or 'required'
        """
        self.message_history.append(
            Message(
                content=message,
                role="user"
            )
        )

        kwargs = {
            "message_history" : self.message_history,
            "model" : model,
            "tools" : self.tools,
            "tool_choice" : tool_choice
        }

        if model == None:
            del kwargs["model"]

        response = self.adaptor.get_completion_with_history(**kwargs)

        self.message_history.append(response)

        if len(response.tool_calls) == 0:
            return response

        self._manage_tool(response)

        kwargs["message_history"] == self.message_history
        kwargs["tool_choice"] == "none"

        response = self.adaptor.get_completion_with_history(**kwargs)

        return response

    
    def send_message_without_history(self, message: str, model: str | None = None, tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        """
        Returns a Message object. Message.content to retrieve what the model said\n
        message: the message to send to the model\n
        model: the llm model used. None means use the default model\n
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

        if len(response.tool_calls) == 0:
            return response

        message_history = [response] + self._manage_tool_no_history(response)

        response = self.adaptor.get_completion

        return response

    def _manage_tool(self, message: Message) -> None:
        if len(message.tool_calls) == 0:
            raise ValueError("This function should only be called if there are tool calls")
        
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
        """
        returns a list of responsese from the tools\n
        the list is usually len()=1 because there is usually only 1 tool call
        """
        if len(message.tool_calls) == 0:
            raise ValueError("This function should only be called if there are tool calls")
        
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