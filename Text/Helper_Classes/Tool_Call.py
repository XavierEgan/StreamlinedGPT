class Tool_Call:
    def __init__(self, id: str, name: str, type: str, arguments: str):
        if not type == "function":
            raise TypeError(f"type should probably be 'function', not {type}")

        self.id = id
        self.name = name
        self.type = type
        # arguments is a json string so we can just store it as a string
        self.arguments = arguments