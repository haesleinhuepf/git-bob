def example_function(param1, param2):
    """
    This is an example function that performs a specific task.

    Parameters
    ----------
    param1 : int
        The first parameter, which could be an integer value.
    param2 : str
        The second parameter, which should be a string.

    Returns
    -------
    result : bool
        The result of the function which will be a boolean.

    Examples
    --------
    >>> example_function(10, 'test')
    True
    """
    return True

def github_api_call(api_endpoint, params=None):
    """
    Makes a call to the GitHub API and returns the response.

    Parameters
    ----------
    api_endpoint : str
        The endpoint of the GitHub API that you wish to call.
    params : dict, optional
        Dictionary of parameters to include in the API request (default is None).

    Returns
    -------
    response : dict
        The response from the GitHub API as a dictionary.

    Examples
    --------
    >>> github_api_call('/repos/owner/repo')
    {'id': 123, 'name': 'repo', 'full_name': 'owner/repo'}
    """
    response = {}  # This would typically be a response from the API call
    return response

def parse_github_issue(issue):
    """
    Parses the information from a GitHub issue.

    Parameters
    ----------
    issue : dict
        A dictionary containing issue data retrieved from the GitHub API.

    Returns
    -------
    parsed_issue : dict
        Dictionary containing parsed issue information.

    Examples
    --------
    >>> issue_data = {'id': 86, 'title': 'Example Issue', 'state': 'open'}
    >>> parse_github_issue(issue_data)
    {'id': 86, 'title': 'Example Issue', 'status': 'open'}
    """
    parsed_issue = {
        'id': issue['id'],
        'title': issue['title'],
        'status': issue['state']
    }
    return parsed_issue