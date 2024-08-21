from .Library import StreamlinedGPT

class prebuiltTools:
    def __init__(self):
        self.runPythonCode = StreamlinedGPT.tool(
            function=self._execute,
            name="execute",
            description="execute python code. Returns a dictionary of every variable in the code. In order to get information out, set a global variable which will be returned",
            arguments=[
                StreamlinedGPT.tool.argument("code", "string", "the code that is ran")
            ]
        )

    def _execute(self, code):
        localDict = {}

        try:
            exec(code, None, localDict)
        except Exception as e:
            return f"code had an error: {e}"
        
        returnDict = {}

        # exclude functions, classes, objects etc because it will break everything if they are returned
        for key, value in iter(localDict.items()):
            if type(value) in [str, int, float, list, dict, set, tuple]:
                returnDict[key] = value

        return returnDict
    
    def autoPrompt(promptList):
        tempAssistant = StreamlinedGPT.assistant("You are a helpfull assistant. for anything relating to math, counting, problems etc, use the code editor when appropriate.", "gpt-4o-mini")
        tempAssistant.addTool(prebuiltTools().runPythonCode)
        for prompt in promptList:
            # print(StreamlinedGPT.getResponse(f"write the following prompt, but write the action that is taking place. For example if the prompt was count the instances of the letter r, the output should be 'counting r's' {prompt}", "gpt-4o-mini"))
            tempAssistant.addUserMessageToHistory(prompt)
            tempAssistant.getAiResponse()
        tempAssistant.addUserMessageToHistory("recap the reasoning you just went to and give a final answer")
        tempAssistant.getAiResponse()
        tempAssistant.addUserMessageToHistory("check 1 more time to ensure the answer is correct and recap it again.")
        return tempAssistant.getAiResponse()