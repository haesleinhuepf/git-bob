"""
GitBob AI GitHub Utilities

This module provides utility functions for interacting with GitHub using the GitBob AI framework.
"""

import requests

def get_issue_comments(issue_url):
    """
    Retrieve comments from a GitHub issue.

    Parameters
    ----------
    issue_url : str
        The URL of the GitHub issue.

    Returns
    -------
    list
        A list of dictionaries containing the comments on the issue.
    """
    response = requests.get(issue_url)
    response.raise_for_status()
    return response.json()

def create_issue(repo_url, title, body):
    """
    Create a new issue in a GitHub repository.

    Parameters
    ----------
    repo_url : str
        The URL of the GitHub repository.
    title : str
        The title of the issue.
    body : str
        The body content of the issue.

    Returns
    -------
    dict
        A dictionary containing the created issue data.
    """
    data = {
        'title': title,
        'body': body
    }
    response = requests.post(repo_url, json=data)
    response.raise_for_status()
    return response.json()