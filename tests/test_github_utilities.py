from git_bob._github_utilities import get_github_repository

def test_get_github_repository():
    assert get_github_repository("haesleinhuepf/git_bob").name == "git_bob"

def test_get_github_issue():
    assert False

def test_get_github_pull_request():
    pass

def test_create_github_pull_request():
    pass

def test_update_github_pull_request():
    pass

def test_get_github_file_content():
    pass

def test_update_github_file():
    pass