from github import Github
import os

def get_github_issue(issue_number):
    """
    Retrieve a GitHub issue by its number.

    Parameters
    ----------
    issue_number : int
        The number of the issue to retrieve.

    Returns
    -------
    github.Issue.Issue
        The GitHub issue object.

    Raises
    ------
    Exception
        If the GitHub token is not set or the issue cannot be retrieved.
    """
    token = os.environ.get("GITHUB_TOKEN")
    if token is None:
        raise Exception("GITHUB_TOKEN environment variable not set")
    
    g = Github(token)
    repo = g.get_repo("haesleinhuepf/git-bob")
    return repo.get_issue(issue_number)

def get_issue_summary(issue):
    """
    Generate a summary of a GitHub issue.

    Parameters
    ----------
    issue : github.Issue.Issue
        The GitHub issue object.

    Returns
    -------
    str
        A formatted summary of the issue.
    """
    return f"""Summary of Issue #{issue.number} in {issue.repository.full_name} repository:

Title: {issue.title}

Key points:
{issue.body}
"""

def get_file_content(issue, filename):
    """
    Retrieve the content of a file from the repository.

    Parameters
    ----------
    issue : github.Issue.Issue
        The GitHub issue object.
    filename : str
        The name of the file to retrieve.

    Returns
    -------
    str
        The content of the file.

    Raises
    ------
    Exception
        If the file cannot be found in the repository.
    """
    repo = issue.repository
    try:
        content = repo.get_contents(filename)
        return content.decoded_content.decode()
    except:
        raise Exception(f"File {filename} not found in repository")