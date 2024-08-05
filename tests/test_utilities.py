from git_bob._utilities import remove_indentation, remove_outer_markdown

def test_remove_indentation():
    assert remove_indentation("    Hello") == "Hello"
    assert remove_indentation("        Hello") == "    Hello"

def test_remove_outer_markdown():
    assert remove_outer_markdown("""```python
bla
```""") == "bla"

def test_function3():
    pass

# Add more test functions as needed for other functions in _utilities.py