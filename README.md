# StreamlinedGPT
StreamlinedGPT is a custom OpenAI Library that allows for easy interaction with the OpenAI API and management of tools. It sacrifices functionality for ease of use and maintainability.

## Quick Start
skip to step 5 if you already have your API key set as a system variable

### Step 1: Create OpenAI Account
go to https://platform.openai.com/docs/overview and set up an account

### Step 2: Add Money To Account
press the gear in the top right corner\
press billing on the menu to the left\
press `Add to credit balance`\
you do not need much money, a single dollar will last you aproximetly 937500 words for GPT-4o-mini

### Step 3: Create API key
press dashboard on the top right corner\
press API keys\
press `+ Create new secret key`
copy this key - DO NOT SHARE IT WITH ANYONE

### Step 4: use API key
there are two ways to get the API key into python.
### Option 1: Put in secrets file
in the StreamlinedGPT > secrets > OpenAiKey.py set the `key` variable to your api key (as a string)
```Python
key = "uh78g40w8g4hwbg0ui456h8u0yg2h08g2456082345"
```
make sure you dont accidentally push your key.

### Option 2: Set system variable
press the windows key and type "system var", then press `Edit the system environment variables`
press `advanced` in the top menu
press `Environment Variables...`
press `New...` that is below the top box
name it `OPENAI_API_KEY` and make its value your api key
the library should now work


### Step 5: Download the library
press the green `<> code` button
press download zip
extract the zip in the same folder as where you want to code

### Step 6: Download requirements
copy the full path to the `requirements.txt` file and run the following command in a terminal `pip install -r "/path/to/your/project/requirements.txt"`

### Step 7: Import the library
in python type `from StreamlinedGPT.Library import StreamlinedGPT`. This will give you the StreamlinedGPT class, which is explained below.


below is a simple example showing how the library is intended too be used. It defines "calculator" and then builds a tool the Ai can use.
```python
from StreamlinedGPT.Library import StreamlinedGPT

# create a function/tool the AI will have access to
def calculator(expression: str):
    try:
        return eval(expression)
    except Exception as e:
        return f"error: {e}"

# create an assistant with a system message and model (full list of models can be found on OpenAI's website)
assistant = StreamlinedGPT.assistant(systemMessage="you are a helpfull assistant", model="gpt-4o-mini")

# add a tool
assistant.addTool(StreamlinedGPT.tool(
    function=calculator, 
    name="calculator", 
    description="give a string and the function will evaluate it",
    arguments=[
        StreamlinedGPT.tool.argument(name="expression", type="string", description="the expression that is evaluated")
    ]
))

# start a chatloop with the user in the comand line
assistant.chatLoopCLI()
```
below is another example using one of the prebuilt tools
```python
from StreamlinedGPT.Library import StreamlinedGPT
from StreamlinedGPT.prebuilts import prebuiltTools

assistant = StreamlinedGPT.assistant("you are a helpful assistant", "gpt-4o-mini")
assistant.addTool(prebuiltTools().runPythonCode)

assistant.chatLoopCLI()
```
## Documentation
### class `StreamlinedGPT`
#### method `getResponse(message : str, model : str)`
simply gets a response from the model.
#### class `tool(function : str, name : str, description : str, arguments : list)`
represents a tool the model can access. arguments should be a list of StreamlinedGPT.tool.argument(s)\
example
```python
runPythonCode = StreamlinedGPT.tool(
    function=execute,
    name="execute",
    description="execute python code. Returns a dictionary of every variable in the code.",
    arguments=[
        StreamlinedGPT.tool.argument("code", "string", "the code that is ran")
    ]
) 
```

##### class `argument(name : str, type : str, description : str, isRequired : bool)
represents an argument for a tool. Pass into the `arguments` argument of the StreamlinedGPT.tool\
example
```python
StreamlinedGPT.tool.argument("code", "string", "the code that is ran")
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
