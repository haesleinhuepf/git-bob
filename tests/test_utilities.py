from git_bob._utilities import remove_indentation

def test_remove_indentation():
    assert remove_indentation("    Hello") == "Hello"
    assert remove_indentation("        Hello") == "    Hello"

def test_function2():
    pass

def test_function3():
    pass

# Add more test functions as needed for other functions in _utilities.py