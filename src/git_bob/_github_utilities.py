"""Utilities for interacting with GitHub."""

import requests


def get_github_issue_comments(owner: str, repo: str, issue_number: int) -> list[dict]:
    """Get all comments for a given issue.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    issue_number : int
        The issue number.

    Returns
    -------
    list[dict]
        A list of comments for the issue. Each comment is a dictionary with the following keys:
            - `body`: The body of the comment.
            - `user`: The user who created the comment.
            - `created_at`: The date and time the comment was created.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_github_issue(owner: str, repo: str, issue_number: int) -> dict:
    """Get a given issue.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    issue_number : int
        The issue number.

    Returns
    -------
    dict
        The issue data.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def create_github_issue(owner: str, repo: str, title: str, body: str) -> dict:
    """Create a new issue.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    title : str
        The title of the issue.
    body : str
        The body of the issue.

    Returns
    -------
    dict
        The issue data.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"title": title, "body": body}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def create_github_comment(owner: str, repo: str, issue_number: int, body: str) -> dict:
    """Create a new comment on a given issue.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    issue_number : int
        The issue number.
    body : str
        The body of the comment.

    Returns
    -------
    dict
        The comment data.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": body}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def get_github_pull_request(owner: str, repo: str, pull_request_number: int) -> dict:
    """Get a given pull request.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    pull_request_number : int
        The pull request number.

    Returns
    -------
    dict
        The pull request data.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_github_pull_request_comments(owner: str, repo: str, pull_request_number: int) -> list[dict]:
    """Get all comments for a given pull request.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    pull_request_number : int
        The pull request number.

    Returns
    -------
    list[dict]
        A list of comments for the pull request. Each comment is a dictionary with the following keys:
            - `body`: The body of the comment.
            - `user`: The user who created the comment.
            - `created_at`: The date and time the comment was created.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()