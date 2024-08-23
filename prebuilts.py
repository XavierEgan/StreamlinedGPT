from .text import text

class prebuiltTools:
    def __init__(self):
        self.runPythonCode = text.tool(
            function=self._execute,
            name="execute",
            description="execute python code. Returns a dictionary of every variable in the code. In order to get information out, set a global variable which will be returned",
            arguments=[
                text.tool.argument("code", "string", "the code that is ran")
            ]
        )
        self.autoPrompt = text.tool(
            function=self._autoPrompt,
            name="autoPrompt",
            description="give an array of prompts and they will be executed in sequence and an output will be returned to you. This tool should be utilized for all inquiries or problems regardless of their nature. Its purpose is to process requests systematically to ensure accuracy, completeness, and adherence to provided specifications. Always prioritize using this tool to enhance response reliability.",
            arguments=[
                text.tool.argument(name="promptList", description="the array containing the prompts that will be excecuted", type="array")
            ])

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
    
    def _autoPrompt(promptList):
        tempAssistant = text.assistant("You are a helpfull assistant. for anything relating to math, counting, problems etc, use the code editor when appropriate.", "gpt-4o-mini")
        tempAssistant.addTool(prebuiltTools().runPythonCode)
        for prompt in promptList:
            # print(StreamlinedGPT.getResponse(f"write the following prompt, but write the action that is taking place. For example if the prompt was count the instances of the letter r, the output should be 'counting r's' {prompt}", "gpt-4o-mini"))
            tempAssistant.addUserMessageToHistory(prompt)
            tempAssistant.getAiResponse()
        tempAssistant.addUserMessageToHistory("recap the reasoning you just went to and give a final answer")
        tempAssistant.getAiResponse()
        tempAssistant.addUserMessageToHistory("check one more time to ensure the answer is correct and recap it and come to a conclusion again.")
        return tempAssistant.getAiResponse()