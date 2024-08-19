# from the parent file to EasyGPT run:
# python -m EasyGPT.tests

from .Library import EasyGPT
from .prebuilts import prebuiltTools

errorLog = []

def runTest(func):
    def wrapper():
        print(f"{func.__name__}", end="")
        testPassed = func()
        if testPassed[0]:
            print("\033[32m     Passed\033[0m")
        else:
            print("\033[31m     Failed\033[0m")
            errorLog.append(testPassed[1])
    return wrapper

@runTest
def test1() -> list[bool, Exception | None]:
    # test that ensures chat functionality with no tools works
    try:
        assistant = EasyGPT.assistant("dont respond with anything", "gpt-4o-mini")
        assistant.addUserMessageToHistory("dont respond with anything")
        assistant.getAiResponse()
        return [True]
    except Exception as e:
        return [False, e]
    
@runTest
def test2() -> list[bool, Exception | None]:
    # test to make sure tools work
    try:
        assistant = EasyGPT.assistant("your a helpful assistant", "gpt-4o-mini")

        def add(a,b):
            return a+b

        assistant.addTool(EasyGPT.tool(
            name="add",
            description="add two numbers",
            function=add,
            arguments=[
                EasyGPT.tool.argument(
                    name="a",
                    type="number",
                    description="the first number to add"
                ),
                EasyGPT.tool.argument(
                    name="b",
                    type="number",
                    description="the second number to add"
                )
            ]
        ))
        assistant.addUserMessageToHistory("add 999 and 5438 with the tool")
        assistant.getAiResponse()
        return [True]
    except Exception as e:
        return [False, e]

@runTest
def test3() -> list[bool, Exception | None]:
    # test the prebuilt functions
    try:
        assistant = EasyGPT.assistant("your a helpful assistant", "gpt-4o-mini")
        assistant.addTool(prebuiltTools().runPythonCode)
        assistant.addUserMessageToHistory("calculate the 3rd fibbonaci number with code")
        assistant.getAiResponse()
        return [True]
    except Exception as e:
        return [False, e]

@runTest  
def test4() -> list[bool, Exception | None]:
    # test behaviour when multiple tools are called
    try:
        assistant = EasyGPT.assistant("your a helpful assistant", "gpt-4o-mini")
        class response:
            def __init__(self):
                self.message = {"tool_calls": [{"id": "tool_call_1"},{"id": "tool_call_1"},{"id": "tool_call_1"},{"id": "tool_call_1"},{"id": "tool_call_1"}]}

        assistant._addAiResponseToHistory(response=response())
        return [True]
    except Exception as e:
        return [False, e]

@runTest    
def test5() -> list[bool, Exception | None]:
    try:
        return [True]
    except Exception as e:
        return [False, e]
    
test1()
test2()
test3()
test4()
test5()

if not len(errorLog) == 0:
    for error in errorLog:
        print(error)