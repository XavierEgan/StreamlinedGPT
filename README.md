# EasyGPT
custom OpenAI API that makes it a lot easiser

## Documentations
##### ill write proper docs later
examples: chatbot
this is a lot easier than using the api directly.
```python
from EasyGPT.Library import EasyGPT

def whatImThinking():
    return "I am thinking about how to make this code better."

assistantObj = EasyGPT.assistant("you are a helpful assistant", "gpt-4o-mini")
assistantObj.addTool(EasyGPT.tool(whatImThinking, "whatImThinking", "tells you what the user is thinking", []))

while True:
    request = input("USER > ")
    assistantObj.addUserMessageToHistory(request)
    response = assistantObj.getResponseWithHistory()
    print(f"ASSISTANT > {response}")
```
