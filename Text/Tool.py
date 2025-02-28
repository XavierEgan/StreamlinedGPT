from Text.Argument import Argument

class Tool:
    def  __init__(self, function: callable, name: str, description: str, arguments: list[Argument]):
        self.function = function
        self.name = name
        self.description = description
        self.arguments = arguments
    
    def get_tool_string(self) -> str:
        # TODO: this was made for openai, so i should get rid of this and move it to the openai adaptor.
        # extract the arguments
        arguments = {}
        for argument in self.arguments:
            if argument.type == "array":
                arguments[argument.name] = {
                    "type" : argument.type,
                    "items" : {
                        "type" : f"{argument.list_type}"
                    },
                    "description" : argument.description
                }
            else:
                arguments[argument.name] = {
                    "type" : argument.type,
                    "description" : argument.description
                }
        
        # build the tool description for the ai
        toolString = {
            "type" : "function",
            "function" : {
                "name" : self.name,
                "description" : self.description,
                "parameters" : {
                    "type" : "object",
                    "properties" : arguments,
                    "required" : [i.name for i in self.arguments if i.is_required],
                    "additionalProperties" : False
                }
            }
        }