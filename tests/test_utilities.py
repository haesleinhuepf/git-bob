
def test_remove_outer_markdown():
    from git_bob._utilities import remove_outer_markdown
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


def test_create_or_modify_file_ipynb():
    from git_bob._utilities import erase_outputs_of_code_cells
    import json

    # Mock notebook content
    notebook_content = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "outputs": [{"output_type": "stream", "text": "Hello, World!"}]
            }
        ]
    }

    file_content = json.dumps(notebook_content)
    modified_content = erase_outputs_of_code_cells(file_content)

    # Check if output is removed and execution_count is None
    modified_notebook = json.loads(modified_content)
    assert modified_notebook["cells"][0]["outputs"] == []
    assert modified_notebook["cells"][0]["execution_count"] is None

def test_modify_discussion():
    from git_bob._utilities import modify_discussion
    discussion = """
    Check this issue hhttps://github.com/haesleinhuepf/git-bob/pull/1 ,
    this PR https://github.com/haesleinhuepf/git-bob/pull/3 ,
    this file https://github.com/haesleinhuepf/bia-bob/blob/main/setup.cfg and
    this website https://haesleinhuepf.github.io/ 
    """
    modified_discussion = modify_discussion(discussion)
    assert "Hi, this is a test!" in modified_discussion
    assert "I have a question. What" in modified_discussion
    assert "Bug Tracker = https://github.com/haesleinhuepf/bia-bob/issues" in modified_discussion
    assert "Dr. rer. medic. Robert Haase" not in modified_discussion


def test_append_result():
    from git_bob._utilities import append_result
    assert append_result("""
blabla 

```java
ddddd
""", """```java
eeeee
fffff
""") == '\nblabla \n\n```java\nddddd\n\neeeee\nfffff\n'


def test_clean_output1():
    test = """
```markdown
git-bob comment

A more descriptive name for the variable `res` could be `pull_request_response`. Here's how you could update the code:

```python
# Previous code
res = send_pull_request(repository, branch, f"Add {filename}", "") 
print("Done.", res)

@decorator
def function():
    pass

# Updated code
pull_request_response = send_pull_request(repository, branch, f"Add {filename}", "") 
print("Done.", pull_request_response)
```

Just tagging strangers: @anyoneelse and friends: @haesleinhuepf

```
    """
    from git_bob._utilities import clean_output
    result = clean_output("haesleinhuepf/git-bob", test)

    print(result)

    assert "```markdown" not in result
    assert "@haesleinhuepf" in result # tags to friends are kept
    assert "@decorator" in result # decorators in code are kept
    assert "@anyoneelse" not in result # tags to strangers are removed



def test_clean_output2():
    test = """
    blabla
```
    """
    reference = test = """
blabla
```
    """

    from git_bob._utilities import clean_output
    result = clean_output("haesleinhuepf/git-bob", test)

    assert test == reference