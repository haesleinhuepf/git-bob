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
    discussion = "Check this issue https://github.com/user/repo/issues/1 and this PR https://github.com/user/repo/pull/2"
    modified_discussion = modify_discussion(discussion)
    assert "issue" in modified_discussion
    assert "pull_request" in modified_discussion
