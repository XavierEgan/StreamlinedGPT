from openai import OpenAI
import json

try:
    client = OpenAI()
except:
    from .secrets.OpenAiKey import key
    client = OpenAI(api_key=key)

class StreamlinedGPT:
    class tool:
        def  __init__(self, function, name : str, description : str, arguments : list):
            self.function = function
            self.name = name
            self.description = description
            self.arguments = arguments
            

        class argument:
            '''
            name: the name of the argument
            type: "array", "string", "number", "boolean"
            description: the description of the argument that is given to the model. Specify what it does and when and how the model should use it.
            '''
            def __init__(self, name : str, type : str, description : str, isRequired : bool = True, listType = "string"):
                if not type.lower() in ["array", "string", "number", "boolean"]:
                    raise TypeError("type is wrong")
                self.name = name
                self.type = type
                self.description = description
                self.isRequired = isRequired
                self.listType = listType
    
    def getResponse(message, model):
        messages = [{
            "role" : "user",
            "content" : f"{message}"
        }]

        return client.chat.completions.create(
            model=f"{model}",
            messages=messages
        ).choices[0].message.content
    

    class assistant:
        def __init__(self, systemMessage : str, model : str, maxToolCall : int = 5):
            self.systemMessage = systemMessage
            self.model = model
            self.tools = []
            self.messageHistory = [{"role": "system", "content": systemMessage}]
            self.toolLog = {}
            self.maxFunctionCalls = maxToolCall
            self.toolCallCount = 0

        def addTool(self, tool : object):
            # extract the arguments
            arguments = {}
            for argument in tool.arguments:
                if argument.type == "array":
                    arguments[argument.name] = {
                        "type" : argument.type,
                        "items" : {
                            "type" : f"{argument.listType}"
                        },
                        "description" : argument.description
                    }
                else:
                    arguments[argument.name] = {
                        "type" : argument.type,
                        "description" : argument.description
                    }

            # build the tool description for the ai
            toolString = {
                    "type" : "function",
                    "function" : {
                        "name" : tool.name,
                        "description" : tool.description,
                        "parameters" : {
                            "type" : "object",
                            "properties" : arguments,
                            "required" : [i.name for i in tool.arguments if i.isRequired],
                            "additionalProperties" : False
                        }
                    }
                }
            
            # add the tool to the tools list
            self.tools.append(toolString)

            # add the tool to the tool log
            self.toolLog[tool.name] = tool.function
        
        def addUserMessageToHistory(self, message : str):
            self.messageHistory.append({
                "role": f"user",
                "content": f"{message}"
            })

        def getAiResponse(self):
            if len(self.toolLog) == 0:
                aiResponse = self._getAiResponse(tools=False)
            else:
                if self.toolCallCount >= self.maxFunctionCalls:
                    aiResponse = self._getAiResponse(tools=False)
                else:
                    aiResponse = self._getAiResponse()

            self._addAiResponseToHistory(aiResponse)

            if aiResponse.finish_reason in ["stop", "length", "content_filter"]:
                return(aiResponse.message.content)

            elif aiResponse.finish_reason == "tool_calls":
                self._manageTool(aiResponse)
                return self.getAiResponse()
            
            else:
                print("ai's stop reason was unexpected (probably a function call)")
        
        def chatLoopCLI(self):
            while True:
                userMessage = input("USER > ")
                self.addUserMessageToHistory(userMessage)
                print(f"ASSISTANT > {self.getAiResponse()}")
        
        def _getAiResponse(self, tools: bool = True):
            if tools:
                self.toolCallCount += 1
                return client.chat.completions.create(
                    model=f"{self.model}",
                    messages=self.messageHistory,
                    tools=self.tools
                ).choices[0]
            else:
                self.toolCallCount += 1
                return client.chat.completions.create(
                    model=f"{self.model}",
                    messages=self.messageHistory
                ).choices[0]

        def _addAiResponseToHistory(self, response : object):
            self.messageHistory.append(response.message)

        def _manageTool(self, aiResponse):
            for call in range(len(aiResponse.message.tool_calls)):
                toolCall = aiResponse.message.tool_calls[call].function

                try:
                    toolResponse = self.toolLog[toolCall.name](**json.loads(toolCall.arguments))
                except Exception as e:
                    toolResponse = f"the following error occured: {e}"
                
                self._addToolResponseToHistory(aiResponse, toolResponse, call)

        def _addToolResponseToHistory(self, aiResponse, toolResponse, toolCallId):
            self.messageHistory.append({
                "role": "tool",
                "content": json.dumps({
                    "result": toolResponse
                }),
                "tool_call_id": aiResponse.message.tool_calls[toolCallId].id
            })