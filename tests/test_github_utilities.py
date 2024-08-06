def test_get_github_repository():
    from git_bob._github_utilities import get_github_repository
    assert get_github_repository("haesleinhuepf/git-bob").name == "git-bob"

def test_get_github_issue():
    from git_bob._github_utilities import get_github_issue_details
    assert "Issue #1: Testing conversational workflows" in get_github_issue_details("haesleinhuepf/git-bob", 1)

def test_get_conversation_on_issue():
    from git_bob._github_utilities import get_conversation_on_issue
    conversation = get_conversation_on_issue("haesleinhuepf/git-bob", 20)

    assert "What is the captial of France?" in conversation
    assert "France" in conversation

def test_get_most_recent_comment_on_issue():
    from git_bob._github_utilities import get_most_recent_comment_on_issue
    user, comment = get_most_recent_comment_on_issue("haesleinhuepf/git-bob", 20)

    assert "What is the captial of France?" not in comment
    assert "France" in comment

def test_list_issues():
    from git_bob._github_utilities import list_issues
    closed_issues = list(list_issues("haesleinhuepf/git-bob", state="closed").keys())

    assert 1 in closed_issues
    assert 20 in closed_issues

def test_list_repository_files():
    from git_bob._github_utilities import list_repository_files
    files = list(list_repository_files("haesleinhuepf/git-bob"))

    assert "readme.md" in files
    assert "LICENSE" in files
    assert "src/git_bob/__init__.py" in files
    assert "playground/python_basics.ipynb" in files

def test_get_repository_file_contents():
    from git_bob._github_utilities import get_repository_file_contents
    content = get_repository_file_contents("haesleinhuepf/git-bob", ["readme.md"])

    assert len(list(content.keys())) == 1
    assert "readme.md" in list(content.keys())
    assert content["readme.md"].startswith("# git-bob")
    assert "## Acknowledgements" in content["readme.md"]

def test_check_if_file_exists():
    from git_bob._github_utilities import check_if_file_exists
    assert check_if_file_exists("haesleinhuepf/git-bob", "main", "readme.md")
    assert not check_if_file_exists("haesleinhuepf/git-bob", "main", "readme2.md")

def test_create_or_modify_file():
    from git_bob._github_utilities import create_or_modify_file
    import json

    # Mock file content for a Jupyter notebook
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

    # Call the function (assuming it returns the modified content)
    modified_content = create_or_modify_file("haesleinhuepf/git-bob", "test.ipynb", file_content, "Test commit")

    # Parse the modified content
    modified_notebook = json.loads(modified_content)

    # Check if outputs and execution_count are removed
    assert modified_notebook['cells'][0]['outputs'] == []
    assert modified_notebook['cells'][0]['execution_count'] is None
