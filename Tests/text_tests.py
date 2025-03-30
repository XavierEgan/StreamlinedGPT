from ..Text.Openai_Adaptor import Openai_Adaptor

def Openai_Adaptor_initial_test():
    openai = Openai_Adaptor()
    test = openai.get_completion("hello")
    print(test.content)