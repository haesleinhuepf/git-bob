def quick_first_response(repository, issue):
    """
    Response to a comment to the GitHub issue just mentioning that we're on it.

    Parameters
    ----------
    message : str
        The error message to be reported.
    """
    from ._config import Config

    # add reaction to issue
    Config.git_utilities.add_reaction_to_last_comment_in_issue(repository, issue, "+1")


def is_github_url(url):
    """
    Check if the given URL is a GitHub URL and determine its type.
    """
    from ._config import Config, IMAGE_FILE_ENDINGS

    if not str(url).startswith(Config.git_server_url):
        return None
    if "/.github" in url:
        return None
    if ".gitlab-ci.yml" in url:
        return None
    if '/issues/' in url:
        return 'issue'
    elif '/pull/' in url:
        return 'pull_request'
    elif any([url.endswith(f) for f in IMAGE_FILE_ENDINGS]) \
            or url.endswith('.webp') or "user-attachments/assets" in url or url.endswith("?raw=true"):
        return 'image'
    elif url.endswith('.csv') or url.endswith('.xlsx') or url.endswith('.tif') or url.endswith('.zip') or url.endswith('.svg') or url.endswith('.xml'):
        return 'data'
    elif 'blob/' in url:
        return 'file'
    return None