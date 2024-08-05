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

def test_update_github_file():
    pass