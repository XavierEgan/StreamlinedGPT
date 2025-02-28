from Tool_Call import Tool_Call

class Message:
    def __init__(self, content: str, role: str, tool_calls: list[Tool_Call]):
        if len(tool_calls) > 0 and content != None:
            raise ValueError("`content` must be None if `len(tool_calls)`>0")

        if not role in ["user", "developer", "assistant"]:
            raise ValueError(f"role must be either 'user', 'developer' or 'assistant'. not: {role}")

        self.content = content
        self.role = role
        self.tool_calls = tool_calls