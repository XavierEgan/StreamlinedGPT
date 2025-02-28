# https://www.geeksforgeeks.org/decorators-in-python/
def run_test(test_name: str):
    def decorator(test: callable):
        def wrapper():
            print()
            test_result = test()
        return wrapper
    return decorator
