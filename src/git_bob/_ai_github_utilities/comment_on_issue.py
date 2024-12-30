import logging

from github import Github, GithubException

from git_bob._ai_github_utilities.utilities import (
    get_github_token,
    get_repository_from_environment,
    handle_github_exception,
)


def comment_on_issue(issue_number: int, comment_text: str) -> bool:
    """
    Add a comment to a GitHub issue.

    Parameters
    ----------
    issue_number : int
        The issue number to comment on
    comment_text : str
        The text of the comment to add

    Returns
    -------
    bool
        True if successful, False otherwise
    """
    try:
        token = get_github_token()
        github = Github(token)
        repo = get_repository_from_environment(github)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment(comment_text)
        logging.info(f"Successfully commented on issue #{issue_number}")
        return True

    except GithubException as e:
        handle_github_exception(e)
        return False
