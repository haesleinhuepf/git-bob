import requests

def get_github_issue(owner, repo, issue_number):
    """
    Get the details of a GitHub issue.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    issue_number : int
        The number of the issue.

    Returns
    -------
    dict
        A dictionary containing the issue details.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url)
    return response.json()

def create_github_issue(owner, repo, title, body, token):
    """
    Create a new GitHub issue.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    title : str
        The title of the issue.
    body : str
        The body content of the issue.
    token : str
        The GitHub token for authentication.

    Returns
    -------
    dict
        A dictionary containing the created issue details.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {'Authorization': f'token {token}'}
    data = {
        'title': title,
        'body': body
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def close_github_issue(owner, repo, issue_number, token):
    """
    Close an existing GitHub issue.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo : str
        The name of the repository.
    issue_number : int
        The number of the issue to be closed.
    token : str
        The GitHub token for authentication.

    Returns
    -------
    dict
        A dictionary containing the closed issue details.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {'Authorization': f'token {token}'}
    data = {'state': 'closed'}
    response = requests.patch(url, headers=headers, json=data)
    return response.json()