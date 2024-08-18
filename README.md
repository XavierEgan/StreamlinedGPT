# EasyGPT
custom OpenAI API that allows for easy interaction with the OpenAI API and management of tools. It sacrifices functionality for ease of use and maintainability.

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
represents a tool the model can access

#### class 'assistant'
