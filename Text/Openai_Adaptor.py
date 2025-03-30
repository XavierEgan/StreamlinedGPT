from .Helper_Classes.Text_Adaptor import Text_Adaptor
from .Helper_Classes.Message import Message
from .Helper_Classes.Tool_Call import Tool_Call
from .Tool import Tool
from typing import Literal

from openai import OpenAI
# https://platform.openai.com/docs/api-reference/chat/create?lang=python

# there is a lot of duplicate code in here which i should make helper functions for.
class Openai_Text_Adaptor(Text_Adaptor):
    def __init__(self):
        super().__init__()

        self.client = OpenAI()
    
    def get_completion_with_history(self, message_history: list[Message], model: str = "gpt-4o-mini", tools: list[Tool] = [], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        messages = []
        for message in message_history:
            message_dict = {}
            message_dict["role"] = message.role
            message_dict["content"] = message.content if not message.content == None else ""

            if message.role == "tool":
                message_dict["tool_call_id"] = message.tool_call_id

            tool_calls = []
            if len(message.tool_calls) > 0:
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
            messages.append(message_dict)

        reasoning_effort = None # this handles different reasoning efforts by treating them as different models
        if model.endswith("high"):
            reasoning_effort = "high"
        if model.endswith("medium"):
            reasoning_effort = "medium"
        if model.endswith("low"):
            reasoning_effort = "low"

        kwargs = {
            "model": model,
            "messages": messages,
            "tools": [self._get_tool_string(tool) for tool in tools],
            "tool_choice": tool_choice,
            "reasoning_effort": reasoning_effort
        }

        if reasoning_effort == None:
            del kwargs["reasoning_effort"]
        
        completion = self.client.chat.completions.create(**kwargs)

        tool_calls = []
        if not completion.choices[0].message.tool_calls == None:
            for x in completion.choices[0].message.tool_calls:
                tool_calls.append(Tool_Call(
                    id = x.id, 
                    name = x.function.name, 
                    type = x.type, 
                    arguments=x.function.arguments))

        return Message(
            content = completion.choices[0].message.content,
            role = completion.choices[0].message.role,
            tool_calls = tool_calls
        )

    def get_completion(self, message: str | None, model: str = "gpt-4o-mini", tools: list[Tool] = [], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        messages = [
            {
                "role" : "user",
                "content" : message
            }
        ]
        # copied from get_completion_with_history
        reasoning_effort = None
        if model.endswith("high"):
            reasoning_effort = "high"
        if model.endswith("medium"):
            reasoning_effort = "medium"
        if model.endswith("low"):
            reasoning_effort = "low"
        
        kwargs = {
            "model": model,
            "messages": messages,
            "tools": [self._get_tool_string(tool) for tool in tools],
            "tool_choice": tool_choice,
            "reasoning_effort": reasoning_effort
        }

        if reasoning_effort == None:
            del kwargs["reasoning_effort"]
        
        completion = self.client.chat.completions.create(**kwargs)

        tool_calls = []
        if not completion.choices[0].message.tool_calls == None:
            for x in completion.choices[0].message.tool_calls:
                tool_calls.append(
                    Tool_Call(
                        id = x.id, 
                        name = x.function.name, 
                        type = x.type, 
                        arguments=x.function.arguments
                    )
                )
        
        return Message(
            content = completion.choices[0].message.content,
            role = completion.choices[0].message.role,
            tool_calls = tool_calls
        )
    
    def _get_tool_string(self, tool: Tool):
        # extract the arguments
        arguments = {}
        for argument in tool.arguments:
            if argument.type == "array":
                arguments[argument.name] = {
                    "type" : argument.type,
                    "items" : {
                        "type" : f"{argument.list_type}"
                    },
                    "description" : argument.description
                }
            else:
                arguments[argument.name] = {
                    "type" : argument.type,
                    "description" : argument.description
                }
        
        # build the tool description for the ai
        tool_string = {
            "type" : "function",
            "function" : {
                "name" : tool.name,
                "description" : tool.description,
                "parameters" : {
                    "type" : "object",
                    "properties" : arguments,
                    "required" : [i.name for i in tool.arguments if i.is_required],
                    "additionalProperties" : False
                }
            }
        }
        return tool_string