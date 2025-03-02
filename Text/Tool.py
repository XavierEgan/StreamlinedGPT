from .Argument import Argument

class Tool:
    def  __init__(self, function: callable, name: str, description: str, arguments: list[Argument]):
        self.function = function
        self.name = name
        self.description = description
        self.arguments = arguments