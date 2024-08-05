from git_bob._utilities import remove_indentation, remove_outer_markdown
import pytest

def test_remove_indentation():
    assert remove_indentation("    Hello") == "Hello"
    assert remove_indentation("        Hello") == "    Hello"

def test_remove_outer_markdown():
    assert remove_outer_markdown("""```python
bla
```""") == "bla"

def test_split_content_and_summary():
    from git_bob._utilities import split_content_and_summary
    content, summary = split_content_and_summary("""blabla
                                     
                                     summary""")

    assert content.strip() == "blabla"
    assert summary == "summary"

    content, summary = split_content_and_summary("""blabla

                                         summary
                                         """)

    assert content.strip() == "blabla"
    assert summary == "summary"

@pytest.mark.timeout(1)
def test_timeout_log():
    import time
    time.sleep(2)
