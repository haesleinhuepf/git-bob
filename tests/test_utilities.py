def test_remove_outer_markdown():
    from git_bob._utilities import remove_outer_markdown
    assert remove_outer_markdown("""```python
bla
```""") == "bla"


def test_remove_outer_markdown2():
    # this should stay as it was, because it ends with a comment.
    from git_bob._utilities import remove_outer_markdown
    test_text = """```python
x = 5
```
This sets x to 5."""
    assert remove_outer_markdown(test_text) == test_text


def test_remove_outer_markdown3():
    # this should stay as it was, because it ends with a comment.
    from git_bob._utilities import remove_outer_markdown
    test_text = """This sets x to 5:
```python
x = 5
```"""
    assert remove_outer_markdown(test_text) == test_text


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
    from git_bob._utilities import Config
    import git_bob._github_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://github.com"

    from git_bob._utilities import modify_discussion
    discussion = """
    Check this issue https://github.com/haesleinhuepf/git-bob/pull/1 ,
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
    from git_bob._utilities import Config
    import git_bob._github_utilities as gu
    Config.git_utilities = gu

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
    from git_bob._utilities import Config
    import git_bob._github_utilities as gu
    Config.git_utilities = gu

    test = """blabla @PETER"""
    reference = """blabla @ PETER"""

    from git_bob._utilities import clean_output
    result = clean_output("haesleinhuepf/git-bob", test)

    assert result == reference

def test_saved_environment():
    import os
    from git_bob._utilities import save_and_clear_environment, restore_environment
    os.environ['TEST_KEY'] = '123'
    saved_env = save_and_clear_environment()
    assert os.environ.get("TEST_KEY") is None
    restore_environment(saved_env)
    assert saved_env.get("TEST_KEY") is not None


def test_file_list_from_commit_message_dict_github():
    from git_bob._utilities import file_list_from_commit_message_dict, Config
    Config.running_in_gitlab_ci = False
    Config.running_in_github_ci = True
    Config.git_server_url = "https://github.com/"
    repository = "haesleinhuepf/git-bob"
    branch_name = "test"
    commit_message_dict = {"new_image.png":"added image",
                           "text_file.txt":"modified text",
                           "playground/plot.jpg":"new plot"}

    result = file_list_from_commit_message_dict(repository, branch_name, commit_message_dict)

    assert len(result) == 3
    assert "![new_image.png](https://github.com/haesleinhuepf/git-bob/blob/test/new_image.png?raw=true)" in result
    assert "[text_file.txt](https://github.com/haesleinhuepf/git-bob/blob/test/text_file.txt)" in result
    assert "![playground/plot.jpg](https://github.com/haesleinhuepf/git-bob/blob/test/playground/plot.jpg?raw=true)" in result

def test_file_list_from_commit_message_dict_gitlab():
    from git_bob._utilities import file_list_from_commit_message_dict, Config
    Config.running_in_gitlab_ci = True
    Config.running_in_github_ci = False
    Config.git_server_url = "https://gitlab.com/"
    repository = "haesleinhuepf/git-bob"
    branch_name = "test"
    commit_message_dict = {"new_image.png":"added image",
                           "text_file.txt":"modified text",
                           "playground/plot.jpg":"new plot"}

    result = file_list_from_commit_message_dict(repository, branch_name, commit_message_dict)

    assert len(result) == 3
    assert "![new_image.png](https://gitlab.com/haesleinhuepf/git-bob/-/raw/test/new_image.png)" in result
    assert "[text_file.txt](https://gitlab.com/haesleinhuepf/git-bob/-/blob/test/text_file.txt)" in result
    assert "![playground/plot.jpg](https://gitlab.com/haesleinhuepf/git-bob/-/raw/test/playground/plot.jpg)" in result


def test_ensure_images_shown():
    from git_bob._utilities import ensure_images_shown

    test = """
    * [bla](bla.png)
    * [blu](blu.txt)
    """
    liste = ["![bla](bla.png)", "[blu](blu.txt)"]

    reference = """
    * ![bla](bla.png)
    * [blu](blu.txt)
    """

    assert reference == ensure_images_shown(test, liste)


def test_get_modified_files():
    from git_bob._utilities import get_file_info, get_modified_files

    file_info = get_file_info()

    with open("test.txt", 'w') as f:
        f.write("hello")
    with open("docs/test.md", 'w') as f:
        f.write("world")
    with open("docs/installation-tutorial.md", "r") as f:
        content = f.read()
    with open("docs/installation-tutorial.md", "w") as f:
        f.write(content)

    files = get_modified_files(file_info)

    assert "test.txt" in files
    assert "docs/test.md" in files
    assert "docs/installation-tutorial.md" in files

    assert len(files) == 3


def test_make_slides():
    from git_bob._utilities import make_slides
    import os
    slides_description = '''[
        {"title": "Slide 1", "content": ["Point A", "Point B"]},
        {"title": "Slide 2", "content": ["Point C", "Point D"]}
    ]'''
    make_slides(slides_description, "test_slides.pptx")
    assert os.path.exists("test_slides.pptx")

    from pptx import Presentation
    presentation = Presentation("test_slides.pptx")
    assert len(presentation.slides) == 2


def test_read_local_files_in_discussion():
    from git_bob._utilities import modify_discussion
    discussion = """
    There is something important README.md
    """
    modified_discussion = modify_discussion(discussion)
    assert "# git-bob ![](logo_32x32.png)" in modified_discussion

