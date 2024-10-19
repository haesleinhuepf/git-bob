import os
from gitlab import Gitlab


def get_gitlab_repository(repository):
    """
    Get the GitLab repository object.

    Parameters
    ----------
    repository : str
        The repository identifier.

    Returns
    -------
    gitlab.v4.objects.Project
        The project object.
    """
    gl = Gitlab(os.getenv('GITLAB_URL', 'https://gitlab.com'),
                private_token=os.getenv('GITLAB_API_KEY'))
    return gl.projects.get(repository)


def add_comment_to_issue(repository, issue, comment):
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
    """
    repo = get_gitlab_repository(repository)
    issue_obj = repo.issues.get(issue)
    issue_obj.notes.create({'body': comment})


def list_issues(repository, state="opened"):
    """
    List all GitLab issues with a defined state on a specified repository.

    Parameters
    ----------
    repository : str
        The repository identifier.
    state : str, optional
        The state of the issues to list (default is "opened").

    Returns
    -------
    dict
        A dictionary mapping issue IDs to their titles.
    """
    repo = get_gitlab_repository(repository)
    return {issue.iid: issue.title for issue in repo.issues.list(state=state)}


def get_most_recently_commented_issue(repository):
    """
    Return the issue number of the issue in a repository with the most recent comment.

    Parameters
    ----------
    repository : str
        The repository identifier.

    Returns
    -------
    int
        The ID of the most recently commented issue.
    """
    repo = get_gitlab_repository(repository)
    issues = repo.issues.list(order_by="updated_at", sort="desc")
    if not issues:
        raise ValueError("No issue found")
    return issues[0].iid


def list_repository_files(repository):
    """
    List all files, including those in subfolders, in a given GitLab repository.

    Parameters
    ----------
    repository : str
        The repository identifier.

    Returns
    -------
    list of str
        A list of file paths.
    """
    repo = get_gitlab_repository(repository)
    files = []
    path_stack = ['']
    
    while path_stack:
        path = path_stack.pop()
        tree = repo.repository_tree(path=path)
        for item in tree:
            if item['type'] == 'blob':
                files.append(item['path'])
            elif item['type'] == 'tree':
                path_stack.append(item['path'])
    return files


def create_issue(repository, title, body):
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

    Returns
    -------
    int
        The ID of the created issue.
    """
    repo = get_gitlab_repository(repository)
    issue_obj = repo.issues.create({'title': title, 'description': body})
    return issue_obj.iid


def get_most_recent_comment_on_issue(repository, issue):
    """
    Retrieve the most recent comment on a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The repository identifier.
    issue : int
        The issue number.

    Returns
    -------
    tuple
        A tuple containing the username of the commenter and the comment text.
    """
    repo = get_gitlab_repository(repository)
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


def get_repository_file_contents(repository, file_paths):
    """
    Retrieve the contents of specified files from a GitLab repository.

    Parameters
    ----------
    repository : str
        The repository identifier.
    file_paths : list of str
        A list of file paths.

    Returns
    -------
    dict
        A dictionary mapping file paths to their contents or error message.
    """
    repo = get_gitlab_repository(repository)
    file_contents = {}

    for file_path in file_paths:
        try:
            file_obj = repo.files.get(file_path=file_path, ref='main')
            file_content = file_obj.decode().decode('utf-8')
            file_contents[file_path] = file_content
        except Exception as e:
            file_contents[file_path] = f"Error accessing {file_path}: {str(e)}"

    return file_contents


def send_pull_request(repository, source_branch, target_branch, title, description):
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

    Returns
    -------
    str
        The URL of the created merge request.
    """
    repo = get_gitlab_repository(repository)

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
