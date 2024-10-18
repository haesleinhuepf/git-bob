import pytest
from unittest.mock import MagicMock, patch
from _gitlab_utilities import (
    get_gitlab_repository, add_comment_to_issue, list_issues,
    get_most_recently_commented_issue,
    list_repository_files, create_issue, get_most_recent_comment_on_issue,
    get_repository_file_contents, send_pull_request
)

@pytest.fixture
def mocked_gitlab():
    with patch('gitlab.Gitlab') as gitlab:
        mock_instance = MagicMock()
        gitlab.return_value = mock_instance
        yield mock_instance

def test_get_gitlab_repository(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_gitlab.projects.get.return_value = mocked_repo
    repo = get_gitlab_repository('example/repo', 'fake_token')
    assert repo == mocked_repo

def test_add_comment_to_issue(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_issue = MagicMock()
    mocked_repo.issues.get.return_value = mocked_issue
    mocked_gitlab.projects.get.return_value = mocked_repo

    add_comment_to_issue('example/repo', 1, 'Test Comment', 'fake_token')
    mocked_issue.notes.create.assert_called_once_with({'body': 'Test Comment'})

def test_list_issues(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_issues = [MagicMock(iid=1, title='Issue 1'), MagicMock(iid=2, title='Issue 2')]
    mocked_repo.issues.list.return_value = mocked_issues
    mocked_gitlab.projects.get.return_value = mocked_repo

    issues = list_issues('example/repo', 'opened', 'fake_token')
    assert issues == {1: 'Issue 1', 2: 'Issue 2'}

def test_get_most_recently_commented_issue(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_issues = [MagicMock(iid=3)]
    mocked_repo.issues.list.return_value = mocked_issues
    mocked_gitlab.projects.get.return_value = mocked_repo

    recent_issue_id = get_most_recently_commented_issue('example/repo', 'fake_token')
    assert recent_issue_id == 3

def test_list_repository_files(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_files = [MagicMock(type='blob', path='file1.py'), MagicMock(type='blob', path='file2.py')]
    mocked_repo.repository_tree.return_value = mocked_files
    mocked_gitlab.projects.get.return_value = mocked_repo

    files = list_repository_files('example/repo', 'fake_token')
    assert files == ['file1.py', 'file2.py']

def test_create_issue(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_issue = MagicMock(iid=10)
    mocked_repo.issues.create.return_value = mocked_issue
    mocked_gitlab.projects.get.return_value = mocked_repo

    issue_id = create_issue('example/repo', 'New Issue', 'New issue description', 'fake_token')
    assert issue_id == 10

def test_get_most_recent_comment_on_issue(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_issue = MagicMock(author={'username': 'issue_author'}, description='Issue Body')
    mocked_comments = [MagicMock(author={'username': 'commenter'}, body='Latest Comment')]
    mocked_issue.notes.list.return_value = mocked_comments
    mocked_repo.issues.get.return_value = mocked_issue
    mocked_gitlab.projects.get.return_value = mocked_repo

    user, text = get_most_recent_comment_on_issue('example/repo', 1, 'fake_token')
    assert user == 'commenter'
    assert text == 'Latest Comment'

def test_get_repository_file_contents(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_file = MagicMock(decode=MagicMock(return_value=b'content'))
    mocked_repo.files.get.return_value = mocked_file
    mocked_gitlab.projects.get.return_value = mocked_repo

    file_contents = get_repository_file_contents('example/repo', ['file1.py'], 'fake_token')
    assert file_contents['file1.py'] == 'content'

def test_send_pull_request(mocked_gitlab):
    mocked_repo = MagicMock()
    mocked_mr = MagicMock(web_url='http://example.com/mr/1')
    mocked_repo.mergerequests.create.return_value = mocked_mr
    mocked_gitlab.projects.get.return_value = mocked_repo

    mr_url = send_pull_request('example/repo', 'branch1', 'main', 'MR Title', 'MR Description'[:65535], 'fake_token')
    assert mr_url == 'Merge Request created: http://example.com/mr/1'
