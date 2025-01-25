def test_get_gitlab_repository():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import get_repository_handle
    assert get_repository_handle("haesleinhuepf/git-bob").name == "git-bob"

def test_get_gitlab_issue():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import get_issue_details
    assert "the world looks good" in get_issue_details("haesleinhuepf/git-bob", 1)

def test_get_conversation_on_issue():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import get_conversation_on_issue
    conversation = get_conversation_on_issue("haesleinhuepf/git-bob", 1)

    assert "the world looks good" in conversation
    assert "France" not in conversation

def test_get_most_recent_comment_on_issue():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import get_most_recent_comment_on_issue
    user, comment = get_most_recent_comment_on_issue("haesleinhuepf/git-bob", 12)

    assert "What is the capital of France?" not in comment
    assert "Berlin" in comment

def test_list_issues():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import list_issues
    closed_issues = list(list_issues("haesleinhuepf/git-bob", state="closed").keys())

    assert 3 in closed_issues
    assert 4 in closed_issues

def test_list_repository_files():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import list_repository_files
    files = list(list_repository_files("haesleinhuepf/git-bob", branch_name="main"))

    assert "README.md" in files
    assert "LICENSE" in files
    assert "src/git_bob/__init__.py" in files
    #assert "playground/python_basics.ipynb" in files

def test_get_repository_file_contents():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import get_repository_file_contents
    content = get_repository_file_contents("haesleinhuepf/git-bob", "main", ["README.md"])

    assert len(list(content.keys())) == 1
    assert "README.md" in list(content.keys())
    assert content["README.md"].startswith("# git-bob")
    assert "## Acknowledgements" in content["README.md"]

def test_check_if_file_exists():
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    from git_bob._gitlab_utilities import check_if_file_exists
    assert check_if_file_exists("haesleinhuepf/git-bob", "main", "README.md")
    assert not check_if_file_exists("haesleinhuepf/git-bob", "main", "readme2.md")

def create_comment_on_issue():
    from git_bob._gitlab_utilities import add_comment_to_issue, create_issue, close_issue
    from git_bob._utilities import Config
    import git_bob._gitlab_utilities as gu
    Config.git_utilities = gu
    Config.git_server_url = "https://gitlab.com"

    new_issue = create_issue("haesleinhuepf/git-bob", "test", "This is a test issue")
    add_comment_to_issue("haesleinhuepf/git-bob", new_issue, "This is a test comment")
    close_issue("haesleinhuepf/git-bob", new_issue)
