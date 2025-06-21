from test import TestClass

def translate():
    t = TestClass("test")
    result = t.MyMethod("test", "en", "ko")
    print(result)