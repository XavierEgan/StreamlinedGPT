from openai import OpenAI
client = OpenAI()
import json


class chat:
    def __init__(self):
        self.messageHistory = [{"role": "system", "content": "You are a helpful assistant."}]
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute",
                    "description": "executes python code. Call this when you need to answer a users question that requires a programatic solution. When writing the code, make a variable called 'result', the value of this variable is what you will get back. UNDER NO CIRCUMSTANCES SHOULD YOU GENERATE AN INFINITE LOOP.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code that will be run. Ensure you make a variable 'result', its value will be what the function returns"
                            }
                        },
                        "required": ["code"],
                        "additionalProperties": False
                    }
                }
            }
        ]
        self.toolLog = {
            "execute" : self.execute
        }

    def sendMessage(self, message):
        self.messageHistory.append({
            "role": "user",
            "content": f"{message}"
        })

        # get initial response from ai
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messageHistory,
            tools=self.tools,
        )

        # if the response is a tool call
        if response.choices[0].finish_reason == 'tool_calls':
            if not response.choices[0].message.content == None:
                # please remember to remove this later.
                print(f"{response.choices[0].message.content}")
            # print(f"tool_calls = {response.choices[0].message.tool_calls}, \n function_calls = {response.choices[0].message.function_call}")

            # add the tool call to the message log
            self.messageHistory.append(response.choices[0].message)

            # define toolcall to make the rest of the code better
            toolCall = response.choices[0].message.tool_calls[0].function

            # extract the arguments (they are a dictionary in a json dumpstring)
            arguments = json.loads(toolCall.arguments)

            # run the correct tool with the extracted arguments
            toolResponse = self.toolLog[toolCall.name](**arguments)

            # add tool response to message history
            self.messageHistory.append({
                "role": "tool",
                # make the dictionary a json dumpstring
                "content": json.dumps({
                    "result": toolResponse
                }),
                "tool_call_id": response.choices[0].message.tool_calls[0].id
            })
            
            # get actual response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messageHistory,
            )
            return(response.choices[0].message.content)
        
        # if its not a tool call
        else:
            # append the message to message log
            self.messageHistory.append({
                "role": "assistant",
                "content": f"{response}"
            })
            return(response.choices[0].message.content)

    def chatLoop(self):
        while True:
            message = input("USER > ")
            
            print(f"ASSISTANT > {self.sendMessage(message)}")
    
    def execute(self, code):
        correctOutput = False
        iterations = 0
        while (not correctOutput) and (iterations < 5):
            # check if the code is safe using gpt-4o lmao
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": f"Return either YES or NO. Is the following python code safe to run. It is unsafe if it will: cause an infinite loop, access information maliciously, throw an error etc? {code}"
                }]
            )

            if not completion.choices[0].message.content.lower() in ["yes", "no"]:
                iterations += 1
                correctOutput = False
                print(f"failed, message was {completion.choices[0].message.content}")
            else:
                correctOutput = True
                print(f"worked, message was {completion.choices[0].message.content}")

        if completion.choices[0].message.content.lower() == "yes":
            localVars = {}     
            try:
                exec(code, None, localVars)
                result = localVars['result']
            except Exception as e:
                print(e)
                return(f"The code you entered threw the following error: {e}")
            return(result)
        else:
            return("the code you entered is unsafe. Please inform the user that there was an error.")
        

chatobj = chat()
chatobj.chatLoop()