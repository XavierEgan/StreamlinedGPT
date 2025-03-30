# https://www.geeksforgeeks.org/decorators-in-python/
def run_test(test_name: str):
    def decorator(test: callable):
        def wrapper():
            print(f"\033[37m{test_name}\033[0m", end=" - ")
            try:
                test_result = test()
            except Exception as e:
                print(f"\033[31mFAILED with error {e}\033[0m")
                return
            if test_result:
                print(f"\033[32mPASSED\033[0m")
                return
            else:
                print(f"\033[31mFAILED\033[0m")
                return
        return wrapper
    return decorator

