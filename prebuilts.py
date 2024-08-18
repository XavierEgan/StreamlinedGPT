from .Library import EasyGPT

class prebuiltTools:
    def __init__(self):
        self.runPythonCode = EasyGPT.tool(
            function=self._execute,
            name="execute",
            description="execute python code. Returns a dictionary of every variable in the code.",
            arguments=[
                EasyGPT.tool.argument("code", "string", "the code that is ran")
            ]
        )

    def _execute(self, code):
        localDict = {}

        exec(code, None, localDict)
        
        returnDict = {}

        # exclude functions, classes, objects etc because it will break everything if they are returned
        for key, value in iter(localDict.items()):
            if type(value) in [str, int, float, list, dict, set, tuple]:
                returnDict[key] = value

        return returnDict