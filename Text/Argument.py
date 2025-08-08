from .Common_Imports import *

class Argument:
    '''
    name: the name of the argument\n
    type: "array", "string", "number", "boolean"\n
    description: the description of the argument that is given to the model.\n
    list_type: the type of data the array should take if the argument is a list.
    '''
    def __init__(self, name: str, type: Literal["array", "string", "number", "boolean"], description: str, is_required: bool = True, list_type = "string"):
        if not type.lower() in ["array", "string", "number", "boolean"]:
            raise TypeError("type is wrong")
        self.name = name
        self.type = type
        self.description = description
        self.is_required = is_required
        self.list_type = list_type