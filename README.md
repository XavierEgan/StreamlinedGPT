# StreamlinedGPT
StreamlinedGPT is a Python library designed to simplify interactions with leading AI models. It provides a unified interface to seamlessly integrate and experiment with various models, removing the complexity of dealing with multiple APIs. The library also streamlines the process of granting AI access to tools, empowering users to leverage AI capabilities in a more dynamic and intuitive way, without the need to handle verbose syntax or repetitive boilerplate code.

Whether you're an individual innovator or an enterprise team, StreamlinedGPT is the perfect solution for experimenting with AI models, tooling workflows, and custom prompts. Its design prioritizes ease of use, aiding rapid prototyping and fostering creativity. By reducing development friction, it enables users to focus on building meaningful applications rather than wrestling with technical details.

## Why use StreamlinedGPT?
StreamlinedGPT is designed to simplify the syntax of existing solutions, like OpenAI's Python library, enabling rapid prototyping of tools, prompts, and experiments.

It addresses the lack of an easy, quick way to experiment with model tooling by eliminating boilerplate code and reducing complexity.

Below is a comparison of StreamlinedGPT and OpenAI's library.

<table>
  <thead>
    <tr>
      <th>StreamlinedGPT</th>
      <th>Equivalent code with Openai</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><pre><code>import StreamlinedGPT<br>
chatbot = StreamlinedGPT.Assistant(
&nbsp;&nbsp;&nbsp;&nbsp;StreamlinedGPT.Openai_Text_Adaptor()
)<br>
chatbot.chatloop()</code></pre></td>
      <td><pre><code>from openai import OpenAI
client = OpenAI()<br>
message_history = []<br>
while True:
&nbsp;&nbsp;&nbsp;&nbsp;user_input = input(&quot;\033[94mUSER &gt; \033[0m&quot;)<br>
&nbsp;&nbsp;&nbsp;&nbsp;if user_input == &quot;exit&quot;:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break<br>
&nbsp;&nbsp;&nbsp;&nbsp;message_history.append(
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&quot;role&quot;: &quot;user&quot;,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&quot;content&quot;: user_input
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}
&nbsp;&nbsp;&nbsp;&nbsp;)<br>
&nbsp;&nbsp;&nbsp;&nbsp;response = client.responses.create(
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;model=&quot;gpt-4o-mini&quot;,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;input = message_history
&nbsp;&nbsp;&nbsp;&nbsp;)<br>
&nbsp;&nbsp;&nbsp;&nbsp;message_history.append(
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&quot;role&quot;: &quot;assistant&quot;,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&quot;content&quot;: response.output_text
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}
&nbsp;&nbsp;&nbsp;&nbsp;)<br>
&nbsp;&nbsp;&nbsp;&nbsp;print(f&quot;\033[92mASSISTANT &gt; \033[0m{response.output_text}&quot;)</code></pre></td>
    </tr>
  </tbody>
</table>


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
press the windows key and type "system var"\
press `Edit the system environment variables`\
press `advanced` in the top menu\
press `Environment Variables...`\
press `New...` that is below the top box\
name it `OPENAI_API_KEY` and make its value your api key
the library should now work


### Step 5: Download the library
press the green `<> code` button
press download zip
extract the zip in the same folder as where you want to code

### Step 6: Download requirements
copy the full path to the `requirements.txt` file and run the following command in a terminal `pip install -r "/path/to/your/project/requirements.txt"`

## Very Quick Start
The below code gives a simple example of how the library can be used
```python
import StreamlinedGPT

chatbot = StreamlinedGPT.Assistant(
    StreamlinedGPT.Openai_Text_Adaptor()
)

chatbot.chatloop()
```
The `Assistant` class takes in an `Adaptor`. In this example the `Openai_Text_Adaptor` was used. Currently the library only has an openai adaptor, however this will be expanded in the future.

Tool use is quite simple with StreamlinedGPT. A tool is a python function that the ai model can call. Below is an example
```python
import StreamlinedGPT

chatbot = StreamlinedGPT.Assistant(
    StreamlinedGPT.Openai_Text_Adaptor()
)

def print_to_console(s):
    print(s)

chatbot.add_tool(
    tool=StreamlinedGPT.Tool(
        function=print_to_console,
        name="print_to_console",
        description="prints something to the console",
        arguments=[
            StreamlinedGPT.Argument(
                name="s", 
                type="string", 
                description="the string to print"
            )
        ]
    )
)

chatbot.chatloop()
```
A tool is defined by making an instance of the `Tool` class, and passing it into the `add_tool` method of an `Assistant`. 

## Documentation
### class `Argument`
A class that represents an argument for a tool.
#### constructor
| Argument    | Type                                            | Description                                                                                 |
| ----------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------- |
| name        | str                                             | The name of the argument                                                                    |
| type        | Literal["array", "string", "number", "boolean"] | The data type of the argument                                                               |
| description | str                                             | The description of the argument that is given to the model                                  |
| is_required | bool                                            | Indicates whether the argument is required. Defaults to `True`                              |
| list_type   | str                                             | The type of data the array should contain if the argument is an array. Defaults to "string" |

### class `Assistant`
A class that provides methods for having chat-like conversations with AI models.
#### constructor
| Argument | Type         | Description                                            |
| -------- | ------------ | ------------------------------------------------------ |
| adaptor  | Text_Adaptor | The text adaptor used to communicate with the AI model |

#### method `send_message`
| Argument    | Type                                | Description                                                |
| ----------- | ----------------------------------- | ---------------------------------------------------------- |
| message     | str                                 | The message to send to the model                           |
| model       | str \| None                         | The LLM model to use. If `None`, the default model is used |
| tool_choice | Literal["none", "auto", "required"] | Controls the model's tool use behavior. Defaults to "auto" |

#### method `send_message_without_history`
| Argument    | Type                                | Description                                                |
| ----------- | ----------------------------------- | ---------------------------------------------------------- |
| message     | str                                 | The message to send to the model                           |
| model       | str \| None                         | The LLM model to use. If `None`, the default model is used |
| tool_choice | Literal["none", "auto", "required"] | Controls the model's tool use behavior. Defaults to "auto" |

#### method `add_tool`
| Argument | Type | Description                      |
| -------- | ---- | -------------------------------- |
| tool     | Tool | The tool to add to the assistant |

#### method `chatloop`
Starts an interactive chat loop in the console.

### class `Tool`
A class that represents a tool that can be used by the AI model.
#### constructor
| Argument    | Type           | Description                                            |
| ----------- | -------------- | ------------------------------------------------------ |
| function    | callable       | The function to be executed when the tool is called    |
| name        | str            | The name of the tool                                   |
| description | str            | The description of the tool that is given to the model |
| arguments   | list[Argument] | A list of arguments that the tool function accepts     |
