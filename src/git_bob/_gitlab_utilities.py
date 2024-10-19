# This file contains utility functions using the gitlab API via python-gitlab:
# https://github.com/python-gitlab/python-gitlab (licensed GPLv3)
#
import os
from functools import lru_cache
from ._logger import Log
import gitlab

@lru_cache(maxsize=1)
def get_gitlab_project(repository):
    """
    Get the GitLab project object.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").

    Returns
    -------
    gitlab.v4.objects.Project
        The GitLab project object.
    """
    access_token = os.getenv('GITLAB_API_KEY')
    gl = gitlab.Gitlab(private_token=access_token)
    return gl.projects.get(repository)

def add_comment_to_issue(repository, issue, comment):
    """
    Add a comment to a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue : int
        The issue ID to add a comment to.
    comment : str
        The comment text to add to the issue.
    """
    Log().log(f"-> add_comment_to_issue({repository}, {issue}, ...)")
    project = get_gitlab_project(repository)
    issue_obj = project.issues.get(issue)
    issue_obj.notes.create({'body': comment})

def get_conversation_on_issue(repository, issue):
    """
    Retrieve the entire conversation (title, body, and comments) of a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue : int
        The issue ID to retrieve the conversation for.

    Returns
    -------
    str
        The conversation string containing the issue title, body, and comments.
    """
    Log().log(f"-> get_conversation_on_issue({repository}, {issue})")
    project = get_gitlab_project(repository)
    issue_obj = project.issues.get(issue)
    conversation = f"Issue Title: {issue_obj.title}\n\nIssue Body:\n{issue_obj.description}\n\n"
    notes = issue_obj.notes.list()
    for note in notes:
        conversation += f"Comment by {note.author['username']}:\n{note.body}\n\n"
    return conversation

def get_most_recently_commented_issue(repository):
    """
    Return the ID of the issue in a project where the last comment was posted.
    """
    Log().log(f"-> get_most_recently_commented_issue({repository})")
    project = get_gitlab_project(repository)
    issues = project.issues.list(order_by='updated_at', sort='desc')
    if not issues:
        raise ValueError("No issues available")
    return issues[0].iid

def get_most_recent_comment_on_issue(repository, issue):
    """
    Retrieve the most recent comment on a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue : int
        The issue ID to retrieve the most recent comment for.

    Returns
    -------
    tuple
        A tuple containing the username of the commenter and the comment text.
    """
    Log().log(f"-> get_most_recent_comment_on_issue({repository}, {issue})")
    project = get_gitlab_project(repository)
    issue_obj = project.issues.get(issue)
    notes = issue_obj.notes.list()
    if notes:
        last_note = notes[-1]
        return last_note.author['username'], last_note.body
    else:
        return issue_obj.author['username'], issue_obj.description

def list_issues(repository: str, state: str = "opened") -> dict:
    """
    List all GitLab issues with a defined state on a specified project.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    state : str, optional
        The issue status: can be "opened", "closed", or "all".

    Returns
    -------
    dict
        A dictionary of issues where keys are issue ids and values are issue titles.
    """
    Log().log(f"-> list_issues({repository}, {state})")
    project = get_gitlab_project(repository)
    issues = project.issues.list(state=state)
    return {issue.iid: issue.title for issue in issues}

def get_gitlab_issue_details(repository, issue_id):
    """
    Fetch details of a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue_id : int
        The ID of the issue to retrieve details for.

    Returns
    -------
    dict
        A dictionary containing issue details such as title and description.
    """
    Log().log(f"-> get_gitlab_issue_details({repository}, {issue_id})")
    project = get_gitlab_project(repository)
    issue = project.issues.get(issue_id)
    return {'title': issue.title, 'description': issue.description}

def list_repository_files(repository, ref='main'):
    """
    List all files in the specified GitLab repository branch.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    ref : str, optional
        The name of the branch to list files from (default is 'main').

    Returns
    -------
    list
        A list of file paths in the repository.
    """
    Log().log(f"-> list_repository_files({repository}, {ref})")
    project = get_gitlab_project(repository)
    items = project.repository_tree(ref=ref, recursive=True)
    return [item['path'] for item in items if item['type'] == 'blob']

def get_repository_file_contents(repository, file_path, ref='main'):
    """
    Get the contents of a file in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    file_path : str
        The path to the file in the repository.
    ref : str, optional
        The name of the branch or tag (default is 'main').

    Returns
    -------
    str
        The content of the file as a string.
    """
    Log().log(f"-> get_repository_file_contents({repository}, {file_path}, {ref})")
    project = get_gitlab_project(repository)
    file = project.files.get(file_path=file_path, ref=ref)
    return file.decode().decode()

def write_file_in_branch(repository, file_path, content, branch, commit_message):
    """
    Write or update a file in a specified branch of a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    file_path : str
        The path to the file to be written or updated.
    content : str
        The content to write into the file.
    branch : str
        The name of the branch to write the changes to.
    commit_message : str
        The commit message associated with the change.

    Returns
    -------
    None
    """
    Log().log(f"-> write_file_in_branch({repository}, {file_path}, {branch})")
    project = get_gitlab_project(repository)
    try:
        file = project.files.get(file_path=file_path, ref=branch)
        file.content = content
        file.save(branch=branch, commit_message=commit_message)
    except gitlab.exceptions.GitlabGetError:
        project.files.create({
            'file_path': file_path,
            'branch': branch,
            'content': content,
            'commit_message': commit_message
        })

def create_branch(repository, branch_name, ref='main'):
    """
    Create a new branch in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str
        The name of the new branch to create.
    ref : str, optional
        The branch or tag name to create the new branch from (default is 'main').

    Returns
    -------
    None
    """
    Log().log(f"-> create_branch({repository}, {branch_name}, {ref})")
    project = get_gitlab_project(repository)
    project.branches.create({'branch': branch_name, 'ref': ref})
