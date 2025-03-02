from .Helper_Classes.Adaptor import Adaptor
from .Helper_Classes.Message import Message
from .Helper_Classes.Tool_Call import Tool_Call
from .Tool import Tool
from typing import Literal

from openai import OpenAI
# https://platform.openai.com/docs/api-reference/chat/create?lang=python

# there is a lot of duplicate code in here which i should make helper functions for.
class Openai_Adaptor(Adaptor):
    def __init__(self):
        super().__init__()

        self.client = OpenAI()
    
    def get_completion_with_history(self, message_history: list[Message], model: str = "gpt-4o-mini", tools: list[Tool] = [], tool_choice: Literal["none", "auto", "required"] = "auto") -> Message:
        messages = []
        for message in message_history:
            message_dict = {}
            message_dict["role"] = message.role
            message_dict["content"] = message.content

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

        reasoning_effort = None # this handles different reasoning efforts by treating them as different models
        if model.endswith("high"):
            reasoning_effort = "high"
        if model.endswith("medium"):
            reasoning_effort = "medium"
        if model.endswith("low"):
            reasoning_effort = "low"

        # im pretty sure that ill get an error if i try to set a reasoning effort with a non-reasoning model so im just gonna do this so i dont have to worry
        if not reasoning_effort == None:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=[tool.get_tool_string() for tool in tools],
                tool_choice = tool_choice,
                reasoning_effort=reasoning_effort
            )
        else:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=[tool.get_tool_string() for tool in tools],
                tool_choice = tool_choice
            )

        tool_calls = []
        if not completion.choices[0].message.tool_calls == None:
            for x in completion.choices[0].message.tool_calls:
                tool_calls.append(Tool_Call(
                    id = x["id"], 
                    name = x["function"]["name"], 
                    type = x["type"], 
                    arguments=x["function"]["arguments"]))

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
        
        if not reasoning_effort == None:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=[tool.get_tool_string() for tool in tools],
                tool_choice = tool_choice,
                reasoning_effort=reasoning_effort
            )
        else:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=[tool.get_tool_string() for tool in tools],
                tool_choice = tool_choice
            )

        tool_calls = []
        if not completion.choices[0].message.tool_calls == None:
            for x in completion.choices[0].message.tool_calls:
                tool_calls.append(
                    Tool_Call(
                        id = x["id"], 
                        name = x["function"]["name"], 
                        type = x["type"], 
                        arguments=x["function"]["arguments"]
                    )
                )
        
        return Message(
            content = completion.choices[0].message.content,
            role = completion.choices[0].message.role,
            tool_calls = tool_calls
        )