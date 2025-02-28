class Argument:
    '''
    name: the name of the argument
    type: "array", "string", "number", "boolean"
    description: the description of the argument that is given to the model.
    list_type: the type of data the array should take if the argument is a list.
    '''
    def __init__(self, name: str, type: str, description: str, is_required: bool = True, list_type = "string"):
        if not type.lower() in ["array", "string", "number", "boolean"]:
            raise TypeError("type is wrong")
        self.name = name
        self.type = type
        self.description = description
        self.is_required = is_required
        self.list_type = list_type