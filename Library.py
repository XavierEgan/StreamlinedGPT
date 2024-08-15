from openai import OpenAI
client = OpenAI()
import json

class easyGPT:

    class tool:
        def  __init__(self, toolFunction, toolName : str, toolDescription : str, arguments : list):
            self.toolFunction = toolFunction
            self.toolName = toolName
            self.toolDescription = toolDescription
            self.arguments = arguments

        class argument:
            '''
            argumentName: the name of the argument
            argumentType: "array", "string", "number", "boolean"
            argumentDescription: the description of the argument that is given to the model. Specify what it does and when and how the model should use it.
            '''
            def __init__(self, argumentName : str, argumentType : str, argumentDescription : str, isRequired : bool = True):
                if not argumentType.lower() in ["array", "string", "number", "boolean"]:
                    raise TypeError("argumentType is wrong")
                self.argumentName = argumentName
                self.argumentType = argumentType
                self.argumentDescription = argumentDescription
                self.isRequired = isRequired
    
    class assistant:
        def __init__(self, systemMessage : str, model : str):
            self.systemMessage = systemMessage
            self.model = model
            self.tools = []
            self.messageHistory = [{"role": "system", "content": systemMessage}]
            self.toolLog = {}

        def addTool(self, tool : object):
            # extract the arguments
            arguments = {}
            for argument in tool.arguments:
                arguments[argument.argumentName] = {
                    "type" : argument.argumentType,
                    "description" : argument.argumentDescription
                }

            # build the tool description for the ai
            toolString = {
                    "type" : "function",
                    "function" : {
                        "name" : tool.toolName,
                        "description" : tool.toolDescription,
                        "parameters" : {
                            "type" : "object",
                            "properties" : arguments,
                            "required" : [i.argumentName for i in tool.arguments if i.isRequired],
                            "additionalProperties" : False
                        }
                    }
                }
            
            # add the tool to the tools list
            self.tools.append(toolString)

            # add the tool to the tool log
            self.toolLog[tool.toolName] = tool.toolFunction
        
        def addUserMessageToHistory(self, message : str):
            self.messageHistory.append({
                "role": f"user",
                "content": f"{message}"
            })

        def getResponseWithHistory(self):

            aiResponse = self._getAiResponse()
            self._addAiResponseToHistory(aiResponse)

            if aiResponse.finish_reason == "stop":
                return(aiResponse.message.content)

            elif aiResponse.finish_reason == "tool_calls":
                self._manageTool(aiResponse)
                return self.getResponseWithHistory()
            
            else:
                print("SOMETHING WENT WRONG AND AI STOPPED WERIDLY")
        
        def _getAiResponse(self, tools: bool = True):
            if tools:
                return client.chat.completions.create(
                    model=f"{self.model}",
                    messages=self.messageHistory,
                    tools=self.tools
                ).choices[0]
            else:
                return client.chat.completions.create(
                    model=f"{self.model}",
                    messages=self.messageHistory
                ).choices[0]

        def _addAiResponseToHistory(self, response : object):
            self.messageHistory.append(response.message)

        def _manageTool(self, aiResponse):
            toolCall = aiResponse.message.tool_calls[0].function

            toolResponse = self.toolLog[toolCall.name](**json.loads(toolCall.arguments))

            self._addToolResponseToHistory(aiResponse, toolResponse)

        def _addToolResponseToHistory(self, aiResponse, toolResponse):
            self.messageHistory.append({
                "role": "tool",
                "content": json.dumps({
                    "result": toolResponse
                }),
                "tool_call_id": aiResponse.message.tool_calls[0].id
            })


if __name__ == "__main__":
    def whatImThinking():
        return "I am thinking about how to make this code better."
    
    assistantObj = easyGPT.assistant("you are a helpful assistant", "gpt-4o-mini")
    assistantObj.addTool(easyGPT.tool(whatImThinking, "whatImThinking", "tells you what the user is thinking", []))

    while True:
        request = input("USER > ")
        assistantObj.addUserMessageToHistory(request)
        response = assistantObj.getResponseWithHistory()
        print(f"ASSISTANT > {response}")