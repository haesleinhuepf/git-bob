import pytest
from unittest.mock import MagicMock
import gitlab_utilities


def test_copy_file_in_repository():
    """Test copying a file within a repository branch."""
    # Setup mocks and input data
    repo_mock = MagicMock()
    repo_mock.files.get.return_value.content = 'example_content'
    gitlab_utilities.get_gitlab_repository = MagicMock(return_value=repo_mock)

    # Call function
    gitlab_utilities.copy_file_in_repository(
        'dummy_repo',
        'main',
        'source/path/file.txt',
        'dest/path/file.txt',
        'Copy file',
        'fake_token'
    )

    # Assert files.create was called
    repo_mock.files.create.assert_called_once_with({
        'file_path': 'dest/path/file.txt',
        'branch': 'main',
        'content': 'example_content',
        'encoding': 'base64',
        'commit_message': 'Copy file'
    })


def test_download_to_repository(requests_mock):
    """Test downloading a file into repository branch."""
    url = 'http://example.com/file.txt'
    requests_mock.get(url, text='file content')

    repo_mock = MagicMock()
    gitlab_utilities.get_gitlab_repository = MagicMock(return_value=repo_mock)

    gitlab_utilities.download_to_repository(
        'dummy_repo',
        'main',
        url,
        'file.txt',
        'fake_token'
    )

    repo_mock.files.create.assert_called_once_with({
        'file_path': 'file.txt',
        'branch': 'main',
        'content': 'file content',
        'commit_message': f"Downloaded {url}, saved as file.txt."
    })


def test_rename_file_in_repository():
    """Test renaming a file within a repository."""
    repo_mock = MagicMock()
    repo_mock.files.get.return_value.content = 'example_content'
    gitlab_utilities.get_gitlab_repository = MagicMock(return_value=repo_mock)

    gitlab_utilities.rename_file_in_repository(
        'dummy_repo',
        'main',
        'old/path/file.txt',
        'new/path/file.txt',
        'Rename file',
        'fake_token'
    )

    repo_mock.files.delete.assert_called_once_with(
        file_path='old/path/file.txt',
        branch='main',
        commit_message='Rename file'
    )

    repo_mock.files.create.assert_called_once_with({
        'file_path': 'new/path/file.txt',
        'branch': 'main',
        'content': 'example_content',
        'encoding': 'base64',
        'commit_message': 'Rename file'
    })


def test_delete_file_from_repository():
    """Test deleting a file from the repository."""
    repo_mock = MagicMock()
    gitlab_utilities.get_gitlab_repository = MagicMock(return_value=repo_mock)

    gitlab_utilities.delete_file_from_repository(
        'dummy_repo',
        'main',
        'file/to/delete.txt',
        'Delete file',
        'fake_token'
    )

    repo_mock.files.delete.assert_called_once_with(
        file_path='file/to/delete.txt',
        branch='main',
        commit_message='Delete file'
    )
