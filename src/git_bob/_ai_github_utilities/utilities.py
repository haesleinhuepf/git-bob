"""
Shared utility functions for AI GitHub operations.
"""

from typing import Any, Dict, Optional

def get_github_api_url(path: str) -> str:
    """
    Construct GitHub API URL for a given path.

    Parameters
    ----------
    path : str
        The API endpoint path

    Returns
    -------
    str
        Complete GitHub API URL
    """
    return f"https://api.github.com/{path.lstrip('/')}"

def build_http_headers(access_token: str) -> Dict[str, str]:
    """
    Build HTTP headers needed for GitHub API requests.

    Parameters
    ----------
    access_token : str
        GitHub access token

    Returns
    -------
    dict
        Headers dictionary
    """
    return {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }

def handle_api_response(response: Any) -> Dict:
    """
    Handle GitHub API response and check for errors.

    Parameters
    ----------
    response : Any
        Response from GitHub API request

    Returns
    -------
    dict
        Response data if successful

    Raises
    ------
    Exception
        If API request failed
    """
    if not response.ok:
        raise Exception(f"GitHub API request failed: {response.status_code} - {response.text}")
    return response.json()
