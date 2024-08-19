from .Library import StreamlinedGPT

class prebuiltTools:
    def __init__(self):
        self.runPythonCode = StreamlinedGPT.tool(
            function=self._execute,
            name="execute",
            description="execute python code. Returns a dictionary of every variable in the code.",
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