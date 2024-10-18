import os
from gitlab import Gitlab


def get_gitlab_repository(repository, private_token):
    """
    Get the GitLab repository object.

    Parameters
    ----------
    repository : str
        The repository identifier.
    private_token : str
        Private token for GitLab API authentication.

    Returns
    -------
    gitlab.v4.objects.Project
        The project object.
    """
    gitlab_url = os.getenv('GITLAB_URL', 'https://gitlab.com')
    gl = Gitlab(gitlab_url, private_token=private_token)
    return gl.projects.get(repository)


def add_comment_to_issue(repository, issue, comment, private_token):
    """
    Add a comment to a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The repository identifier.
    issue : int
        The issue number.
    comment : str
        The comment text.
    private_token : str
        Private token for GitLab API authentication.
    """
    repo = get_gitlab_repository(repository, private_token)
    issue_obj = repo.issues.get(issue)
    issue_obj.notes.create({'body': comment})


def list_issues(repository, state="opened", private_token=None):
    """
    List all GitLab issues with a defined state on a specified repository.

    Parameters
    ----------
    repository : str
        The repository identifier.
    state : str, optional
        The state of the issues to list (default is "opened").
    private_token : str, optional
        Private token for GitLab API authentication (default is None).

    Returns
    -------
    dict
        A dictionary mapping issue IDs to their titles.
    """
    repo = get_gitlab_repository(repository, private_token)
    return {issue.iid: issue.title for issue in repo.issues.list(state=state)}


def get_most_recently_commented_issue(repository, private_token):
    """
    Return the issue number of the issue in a repository with the most recent comment.

    Parameters
    ----------
    repository : str
        The repository identifier.
    private_token : str
        Private token for GitLab API authentication.

    Returns
    -------
    int
        The ID of the most recently commented issue.
    """
    repo = get_gitlab_repository(repository, private_token)
    issues = repo.issues.list(order_by="updated_at", sort="desc")
    if not issues:
        raise ValueError("No issue found")
    return issues[0].iid


def list_repository_files(repository, private_token):
    """
    List all files in a given GitLab repository.

    Parameters
    ----------
    repository : str
        The repository identifier.
    private_token : str
        Private token for GitLab API authentication.

    Returns
    -------
    list of str
        A list of file paths.
    """
    repo = get_gitlab_repository(repository, private_token)
    tree = repo.repository_tree()
    return [item['path'] for item in tree if item['type'] == 'blob']


def create_issue(repository, title, body, private_token):
    """
    Create a new GitLab issue.

    Parameters
    ----------
    repository : str
        The repository identifier.
    title : str
        The issue title.
    body : str
        The issue body.
    private_token : str
        Private token for GitLab API authentication.

    Returns
    -------
    int
        The ID of the created issue.
    """
    repo = get_gitlab_repository(repository, private_token)
    issue_obj = repo.issues.create({'title': title, 'description': body})
    return issue_obj.iid


def get_most_recent_comment_on_issue(repository, issue, private_token):
    """
    Retrieve the most recent comment on a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The repository identifier.
    issue : int
        The issue number.
    private_token : str
        Private token for GitLab API authentication.

    Returns
    -------
    tuple
        A tuple containing the username of the commenter and the comment text.
    """
    repo = get_gitlab_repository(repository, private_token)
    issue_obj = repo.issues.get(issue)
    comments = issue_obj.notes.list(order_by='created_at', sort='desc')

    if comments:
        comment = comments[0]
        user = comment.author['username']
        text = comment.body
    else:
        user = issue_obj.author['username']
        text = issue_obj.description

    if text is None:
        text = ""

    return user, text


def get_repository_file_contents(repository, file_paths, private_token):
    """
    Retrieve the contents of specified files from a GitLab repository.

    Parameters
    ----------
    repository : str
        The repository identifier.
    file_paths : list of str
        A list of file paths.
    private_token : str
        Private token for GitLab API authentication.

    Returns
    -------
    dict
        A dictionary mapping file paths to their contents or error message.
    """
    repo = get_gitlab_repository(repository, private_token)
    file_contents = {}

    for file_path in file_paths:
        try:
            file_obj = repo.files.get(file_path=file_path, ref='main')
            file_content = file_obj.decode().decode('utf-8')
            file_contents[file_path] = file_content
        except Exception as e:
            file_contents[file_path] = f"Error accessing {file_path}: {str(e)}"

    return file_contents


def send_pull_request(repository, source_branch, target_branch, title, description, private_token):
    """
    Create a merge request from a defined branch into the target branch.

    Parameters
    ----------
    repository : str
        The repository identifier.
    source_branch : str
        The name of the source branch.
    target_branch : str
        The name of the target branch.
    title : str
        The title of the merge request.
    description : str
        The description of the merge request.
    private_token : str
        Private token for GitLab API authentication.

    Returns
    -------
    str
        The URL of the created merge request.
    """
    repo = get_gitlab_repository(repository, private_token)

    if len(description) > 65535:
        print("Description is too long. Truncated to 65535 characters. This was the full description:", description)
        description = description[:65535]

    mr = repo.mergerequests.create({
        'source_branch': source_branch,
        'target_branch': target_branch,
        'title': title,
        'description': description
    })

    return f"Merge Request created: {mr.web_url}"
