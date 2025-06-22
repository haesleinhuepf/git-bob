# This file contains utility functions using the github API via github-python:
# https://github.com/PyGithub/PyGithub (licensed LGPL3)
#
import os
from functools import lru_cache
from ._logger import Log

[... CONTENT IDENTICAL UNTIL LINE 621 ...]

def get_diff_of_pull_request(repository, pull_request):
    """
    Get the diff of a specific pull request in a GitHub repository.
    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    pull_request : int
        The pull request number to retrieve the diff for.
    Returns
    -------
    str
        The diff of the pull request.
    """
    import requests

    Log().log(f"-> get_diff_of_pull_request({repository}, {pull_request})")
    # Authenticate with GitHub
    repo = get_repository_handle(repository)
    access_token = os.getenv('GITHUB_API_KEY')

    pull_request = repo.get_pull(pull_request)

    print(pull_request.diff_url)

    # read the content of a url
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(pull_request.diff_url, headers=headers)
    if response.status_code == 200:
        # Return the content of the website
        return response.text
    else:
        print("Error:", response.status_code, response.text)
        return ""

[... REMAINING CONTENT IDENTICAL ...]
