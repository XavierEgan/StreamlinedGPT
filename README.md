# EasyGPT
EasyGPT is a custom OpenAI API that allows for easy interaction with the OpenAI API and management of tools. It sacrifices functionality for ease of use and maintainability.

## Quick Start
below is a simple example showing how the library is intended too be used. It defines "calculator" and then builds a tool the Ai can use.
```python
from EasyGPT.Library import EasyGPT

# create a function/tool the AI will have access to
def calculator(expression: str):
    try:
        return eval(expression)
    except Exception as e:
        return f"error: {e}"

# create an assistant with a system message and model (full list of models can be found on OpenAI's website)
assistant = EasyGPT.assistant(systemMessage="you are a helpfull assistant", model="gpt-4o-mini")

# add a tool
assistant.addTool(EasyGPT.tool(
    function=calculator, 
    name="calculator", 
    description="give a string and the function will evaluate it",
    arguments=[
        EasyGPT.tool.argument(name="expression", type="string", description="the expression that is evaluated")
    ]
))

# start a chatloop with the user in the comand line
assistant.chatLoopCLI()
```
below is another example using one of the prebuilt tools
```python
from EasyGPT.Library import EasyGPT
from EasyGPT.prebuilts import prebuiltTools

assistant = EasyGPT.assistant("you are a helpful assistant", "gpt-4o-mini")
assistant.addTool(prebuiltTools().runPythonCode)

assistant.chatLoopCLI()
```
## Documentation
### class `EasyGPT`
#### class `tool(function : str, name : str, description : str, arguments : list)`
represents a tool the model can access. arguments should be a list of EasyGPT.tool.argument(s)\
example
```python
runPythonCode = EasyGPT.tool(
    function=execute,
    name="execute",
    description="execute python code. Returns a dictionary of every variable in the code.",
    arguments=[
        EasyGPT.tool.argument("code", "string", "the code that is ran")
    ]
) 
```

##### class `argument(name : str, type : str, description : str, isRequired : bool)
represents an argument for a tool. Pass into the `arguments` argument of the EasyGPT.tool\
example
```python
EasyGPT.tool.argument("code", "string", "the code that is ran")
```

#### class `assistant(systemMessage : str, model : str)`
Create an object that enables chatting with the AI and includes conversation history.
##### method `addTool(tool)`
tool should be an instance of the tool class. It gives the assistant access to that tool

##### method `addUserMessageToHistory(message : str)`
adds the user message to the chat history. Do this before calling "getAiResponse"

##### method `getAiResponse()`
returns the response from AI, does not take in any parameters because it looks at the message history (of the assistant it is being called from).

##### method `chatLoopCLI()`
starts a loop in the command line where the user is prompted to input a message, then the assistant responds.
(from quickstart 2)
![image](https://github.com/user-attachments/assets/755c4d20-909a-4efd-953e-087a7951e893)

### class `prebuiltTools`
Class that contains some prebuilt tools that you can use.
