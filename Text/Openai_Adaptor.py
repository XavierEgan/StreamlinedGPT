from Helper_Classes import Adaptor
from Helper_Classes import Message
from Helper_Classes import Tool_Call
from Tool import Tool
from typing import Literal

from openai import OpenAI
# https://platform.openai.com/docs/api-reference/chat/create?lang=python
class Openai_Adaptor(Adaptor):
    def __init__(self):
        super().__init__()

        self.client = OpenAI()
    
    def get_completion_with_history(self, message_history: list[Message], model: str, tools: list[Tool], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        messages = []
        for message in message_history:
            message_dict = {}
            message_dict["role"] = message.role
            message_dict["content"] = message.content
            
            if len(message.tool_calls) > 0:
                tool_calls = []
                for tool_call in message.tool_calls:
                    tool_call_dict = {}
                    tool_call_dict["id"] = tool_call.id
                    tool_call_dict["type"] = tool_call.type
                    tool_call_dict["function"] = {
                        "name" : tool_call.name,
                        "arguments" : tool_call.arguments
                    }
                    tool_calls.append(tool_call_dict)
            
            message_dict["tool_calls"] = tool_calls

        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=[tool.get_tool_string() for tool in tools],
            tool_choice = tool_choice
        )

    def get_completion(self, message: Message, model: str, tools: list[Tool]) -> Message:
        messages = [
            {
                "role" : "user",
                "content" : message.content
            }
        ]