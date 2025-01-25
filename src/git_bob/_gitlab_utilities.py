# This file contains utility functions using the gitlab API via python-gitlab:
# https://github.com/python-gitlab/python-gitlab (licensed GPLv3)
#
import os
from functools import lru_cache
from ._logger import Log
import gitlab

@lru_cache(maxsize=1)
def get_repository_handle(repository):
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
    from ._utilities import Config
    access_token = os.getenv('GITLAB_API_KEY')
    git_server_url = Config.git_server_url
    print("git_server_url", git_server_url)
    print("repository", repository)
    gl = gitlab.Gitlab(url=git_server_url, private_token=access_token)
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
    project = get_repository_handle(repository)
    issue_obj = project.issues.get(issue)
    issue_obj.notes.create({'body': comment})

    print(f"Comment added to issue #{issue} in repository {repository}.")

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
    project = get_repository_handle(repository)
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
    project = get_repository_handle(repository)
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
    from datetime import datetime

    project = get_repository_handle(repository)
    issue_obj = project.issues.get(issue)
    notes = issue_obj.notes.list()

    notes = sorted(notes, key=lambda x: datetime.strptime(x.created_at, '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=False)

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
    project = get_repository_handle(repository)
    issues = project.issues.list(state=state)
    return {issue.iid: issue.title for issue in issues}

def get_issue_details(repository: str, issue: int) -> str:
    """
    Retrieve detailed information about a specific GitLab issue.

    Parameters
    ----------
    repository : str
        The ID or URL-encoded path of the GitLab project.
    issue : int
        The internal ID of the issue to retrieve details for.

    Returns
    -------
    str
        A string containing detailed information about the issue.
    """
    Log().log(f"-> get_gitlab_issue_details({repository}, {issue})")

    # Get the project
    project = get_repository_handle(repository)

    # Fetch the specified issue
    issue = project.issues.get(issue)

    # Format issue details
    content = f"""
Issue #{issue.iid}: {issue.title}
State: {issue.state}
Created at: {issue.created_at}
Updated at: {issue.updated_at}
Closed at: {issue.closed_at}
Author: {issue.author['username']}
Assignees: {', '.join([assignee['username'] for assignee in issue.assignees])}
Labels: {', '.join(issue.labels)}
Comments: {issue.user_notes_count}
Description:
{issue.description}
"""

    # Add comments if any
    if issue.user_notes_count > 0:
        content += "\n\nComments:"
        notes = issue.notes.list()
        for note in notes:
            if not note.system:  # Exclude system-generated notes
                content += f"\n\nComment by {note.author['username']} on {note.created_at}:\n{note.body}"

    return content

def list_repository_files(repository: str, branch_name: str = None, file_patterns:str = None) -> list:
    """
    List all files in the specified GitLab repository branch.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str, optional
        The name of the branch or tag (default is 'main').
    file_patterns : list, optional
        A list of file patterns to filter the files by.

    Returns
    -------
    list
        A list of file paths in the repository.
    """
    if branch_name is None:
        branch_name = get_default_branch_name(repository)

    Log().log(f"-> list_repository_files({repository}, {branch_name})")
    repo = get_repository_handle(repository)
    files = []
    path_stack = ['']

    while path_stack:
        path = path_stack.pop()
        tree = repo.repository_tree(path=path, ref=branch_name)
        for item in tree:
            if item['type'] == 'blob':
                if file_patterns is None or any([f in item['path'].path for f in file_patterns]):
                    files.append(item['path'])
            elif item['type'] == 'tree':
                path_stack.append(item['path'])
    return files

def get_repository_file_contents(repository:str, branch_name, file_paths: list):
    """
    Get the contents of a file in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str, optional
        The name of the branch or tag (default is 'main').
    file_paths : list
        A list of file paths within the repository to retrieve the contents of.


    Returns
    -------
    str
        The content of the file as a string.
    """
    Log().log(f"-> get_repository_file_contents({repository}, {branch_name}, {file_paths})")

    if branch_name is None:
        branch_name = get_default_branch_name(repository)

    project = get_repository_handle(repository)

    file_contents = {}
    for file_path in file_paths:
        try:
            file = project.files.get(file_path=file_path, ref=branch_name)
            file_contents[file_path] = decode_file(file)
        except Exception as e:
            file_contents[file_path] = f"Error accessing {file_path}: {str(e)}"

    return file_contents


def decode_file(file):
    return file.decode().decode()


def write_file_in_branch(repository, branch_name, file_path, new_content, commit_message="Update file"):
    """
    Write or update a file in a specified branch of a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to write the changes to.
    file_path : str
        The path to the file to be written or updated.
    new_content : str
        The content to write into the file.
    commit_message : str
        The commit message associated with the change.

    Returns
    -------
    None
    """
    Log().log(f"-> write_file_in_branch({repository}, {branch_name}, {file_path})")
    import base64

    project = get_repository_handle(repository)

    if isinstance(new_content, bytes):
        new_content = base64.b64encode(new_content).decode('utf-8')

        try:
            file = project.files.get(file_path=file_path, ref=branch_name)
            file.content = new_content
            file.save(branch=branch_name, commit_message=commit_message)
        except gitlab.exceptions.GitlabGetError:
            project.files.create({
                'file_path': file_path,
                'branch': branch_name,
                'content': new_content,
                'encoding': 'base64',
                'commit_message': commit_message
            })
    else:
        try:
            file = project.files.get(file_path=file_path, ref=branch_name)
            file.content = new_content
            file.save(branch=branch_name, commit_message=commit_message)
        except gitlab.exceptions.GitlabGetError:
            project.files.create({
                'file_path': file_path,
                'branch': branch_name,
                'content': new_content,
                'commit_message': commit_message
            })

    # ensure the folder extists
    path_name = str(os.path.dirname(file_path))
    if len(path_name) > 0:
        os.makedirs(path_name, exist_ok=True)
    # save the file
    if isinstance(new_content, bytes):
        with open(file_path, "wb") as f:
            f.write(new_content)
    else:
        with open(file_path, "w") as f:
            f.write(new_content)

    return f"File {file_path} successfully created in repository {repository} branch {branch_name}."


def create_branch(repository, parent_branch=None):
    """
    Create a new branch in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    parent_branch : str
        The branch or tag name to create the new branch from (default is 'main').

    Returns
    -------
    None
    """
    if parent_branch is None:
        parent_branch = get_default_branch_name(repository)

    Log().log(f"-> create_branch({repository}, {parent_branch})")
    import random
    import string
    project = get_repository_handle(repository)
    new_branch_name = "git-bob-mod-" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    project.branches.create({'branch': new_branch_name, 'ref': parent_branch})

    return new_branch_name


def check_if_file_exists(repository, branch_name, file_path):
    """
    Check if a file exists in a given branch of the GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str, optional
        The branch or tag name (default is 'main').
    file_path : str
        The path to the file in the repository.

    Returns
    -------
    bool
        True if the file exists, else False.
    """
    Log().log(f"-> check_if_file_exists({repository}, {branch_name}, {file_path})")
    project = get_repository_handle(repository)
    try:
        project.files.get(file_path=file_path, ref=branch_name)
        return True
    except gitlab.exceptions.GitlabGetError:
        return False

@lru_cache(maxsize=1)
def get_file_in_repository(repository, branch_name, file_path):
    """
    Get a file object from a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str, optional
        The branch or tag name.
    file_path : str
        The path to the file in the repository.

    Returns
    -------
    gitlab.v4.objects.ProjectFile
        The file object.
    """
    Log().log(f"-> get_file_in_repository({repository}, {branch_name}, {file_path})")
    if file_path.endswith(")"):
        file_path = file_path[:-1]
    if file_path.endswith("'"):
        file_path = file_path[:-1]
    if file_path.endswith('"'):
        file_path = file_path[:-1]

    if file_path.endswith("?raw=true"):
        print("fixing file path")
        file_path = file_path[:-9]

    project = get_repository_handle(repository)
    return project.files.get(file_path=file_path, ref=branch_name)

def send_pull_request(repository, source_branch, target_branch, title, description):
    """
    Send a merge request (equivalent to a pull request) in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    source_branch : str
        The name of the branch to merge from.
    target_branch : str
        The name of the branch to merge into.
    title : str
        The title of the merge request.
    description : str
        The description of the merge request.

    Returns
    -------
    gitlab.v4.objects.MergeRequest
        The merge request object.
    """
    Log().log(f"-> send_pull_request({repository}, {source_branch}, {target_branch})")
    project = get_repository_handle(repository)
    mr = project.mergerequests.create({
        'source_branch': source_branch,
        'target_branch': target_branch,
        'title': title,
        'description': description
    })
    return f"Pull request created: {mr.web_url}"

def check_access_and_ask_for_approval(user, repository, issue):
    """
    Check if a user has access to a repository and request approval if needed.

    Parameters
    ----------
    user : str
        The username to check access for.
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue : int
        The issue number related to the access request.

    Returns
    -------
    bool
        True if the user has access, else False.
    """
    Log().log(f"-> check_access_and_ask_for_approval({user}, {repository}, {issue})")
    groups = os.getenv('GIT_BOB_ACCESS_GROUPS', 'members').split(',')

    from ._ai_github_utilities import setup_ai_remark
    access = False
    project = get_repository_handle(repository)

    if "members" in groups:
        members = project.members.list()
        for member in members:
            if member.username == user:
                access = True

    if not access:
        print("User does not have access rights.")

        remark = setup_ai_remark()
        agent_name = os.getenv('AGENT_NAME', 'git-bob')

        add_comment_to_issue(repository, issue, f"""
{remark}

Hi @{user}, 

thanks for reaching out! Unfortunately, I'm not allowed to respond to you directly. 
I need approval from a person who has access.

Best,
{agent_name}
""")
        return False
    return True

def get_contributors(repository):
    """
    Get a list of contributors to a GitLab project.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").

    Returns
    -------
    list
        A list of contributors' usernames.
    """
    Log().log(f"-> get_contributors({repository})")
    project = get_repository_handle(repository)
    contributors = project.repository_contributors()
    return [contributor['name'] for contributor in contributors]

def get_diff_of_pull_request(repository, pull_request):
    """
    Get the diff of a specific merge request in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    pull_request : int
        The ID of the merge request to get the diff for.

    Returns
    -------
    str
        The diff as a string.
    """
    Log().log(f"-> get_diff_of_pull_request({repository}, {pull_request})")
    project = get_repository_handle(repository)
    mr = project.mergerequests.get(pull_request)

    # Get the diff
    diff = mr.changes()['changes']

    output = []

    # Print the diff
    for change in diff:
        output.append(f"File: {change['old_path']} -> {change['new_path']}")
        output.append(change['diff'])
        output.append("\n")

    return "\n".join(output)

def add_reaction_to_issue(repository, issue, reaction="+1"):
    """
    Add a reaction to a specific issue in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue : int
        The ID of the issue to add a reaction to.
    reaction : str
        The emoji code to add as a reaction. Default is "+1".

    Returns
    -------
    None
    """
    Log().log(f"-> add_reaction_to_issue({repository}, {issue}, {reaction})")
    project = get_repository_handle(repository)
    issue = project.issues.get(issue)
    issue.awardemojis.create({'name': reaction})

def add_reaction_to_last_comment_in_issue(repository, issue, reaction="+1"):
    """
    Add a reaction to the last comment in a specific issue in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue : int
        The ID of the issue to add a reaction to the last comment.
    reaction : str
        The emoji code to add as a reaction.

    Returns
    -------
    None
    """
    Log().log(f"-> add_reaction_to_last_comment_in_issue({repository}, {issue}, {reaction})")
    from datetime import datetime
    project = get_repository_handle(repository)
    issue = project.issues.get(issue)
    notes = issue.notes.list()

    notes = sorted(notes, key=lambda x: datetime.strptime(x.created_at, '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=False)

    try:
        if notes:
            last_note = notes[-1]
            last_note.awardemojis.create({"name":reaction})
        else:
            issue.awardemojis.create({"name":reaction})
    except gitlab.exceptions.GitlabCreateError:
        pass # already exists

def get_diff_of_branches(repository, compare_branch, base_branch=None):
    """
    Get the diff between two branches in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    compare_branch : str
        The name of the source branch.
    base_branch : str
        The name of the target branch.

    Returns
    -------
    str
        The diff as a string.
    """

    if base_branch is None:
        base_branch = get_default_branch_name(repository)

    Log().log(f"-> get_diff_of_branches({repository}, {compare_branch}, {base_branch})")
    project = get_repository_handle(repository)
    compare = project.repository_compare(from_=base_branch, to=compare_branch)
    return "\n".join("File:" + diff['old_path'] + " -> " + diff['new_path'] +
                     "\n----------------------------------------\n" +
                     diff['diff'] for diff in compare['diffs'])


def rename_file_in_repository(repository, branch_name, old_file_path, new_file_path, commit_message="Rename file"):
    """
    Rename a file in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str
        The name of the branch where the rename operation will take place.
    old_file_path : str
        The current path of the file.
    new_file_path : str
        The new path of the file.
    commit_message : str
        The commit message associated with the rename.

    Returns
    -------
    None
    """
    Log().log(f"-> rename_file_in_repository({repository}, {old_file_path}, {new_file_path}, {branch_name})")
    project = get_repository_handle(repository)
    file = project.files.get(file_path=old_file_path, ref=branch_name)
    file.path = new_file_path
    file.save(branch=branch_name, commit_message=commit_message)

def delete_file_from_repository(repository, branch_name, file_path, commit_message="Delete file"):
    """
    Delete a file from a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    file_path : str
        The path to the file to delete.
    branch_name : str
        The name of the branch from which to delete the file.
    commit_message : str
        The commit message associated with the delete operation.

    Returns
    -------
    None
    """
    Log().log(f"-> delete_file_from_repository({repository}, {file_path}, {branch_name})")
    project = get_repository_handle(repository)
    project.files.delete(file_path=file_path, branch=branch_name, commit_message=commit_message)

def copy_file_in_repository(repository, branch_name, src_file_path, dest_file_path, commit_message="Copy file"):
    """
    Copy a file within a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    src_file_path : str
        The path to the source file to copy.
    dest_file_path : str
        The destination path for the copied file.
    branch_name : str
        The name of the branch where the copy operation will take place.
    commit_message : str
        The commit message associated with the copy.

    Returns
    -------
    None
    """
    Log().log(f"-> copy_file_in_repository({repository}, {src_file_path}, {dest_file_path}, {branch_name})")
    file_content = decode_file(get_file_in_repository(repository, branch_name, src_file_path))
    write_file_in_branch(repository, branch_name, dest_file_path, file_content, commit_message)

def download_to_repository(repository, branch_name, source_url, target_filename):
    """
    Download a file from a URL and store it in the GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    branch_name : str
        The name of the branch where the file will be added or updated.
    source_url : str
        The URL to download the file from.
    target_filename : str
        The path in the repository where the file will be stored.

    Returns
    -------
    None
    """
    Log().log(f"-> download_to_repository({repository}, {target_filename}, {source_url}, {branch_name})")
    import requests
    import base64

    if source_url.endswith(")"): # happens with ![]() markdown syntax
        source_url = source_url[:-1]

    response = requests.get(source_url)
    if response.status_code == 200:
        file_content = response.content
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

    #encoded_content = base64.b64encode(file_content).decode('utf-8')

    commit_message = f"Downloaded {source_url}, saved as {target_filename}."

    # save the file locally
    with open(target_filename, "wb") as f:
        f.write(file_content)

    write_file_in_branch(repository, branch_name, target_filename, file_content, commit_message)

def create_issue(repository, title, description):
    """
    Create a new issue in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    title : str
        The title of the issue.
    description : str
        The description of the issue.

    Returns
    -------
    gitlab.v4.objects.ProjectIssue
        The issue object.
    """
    Log().log(f"-> create_issue({repository}, {title}, ...)")
    project = get_repository_handle(repository)
    issue = project.issues.create({'title': title, 'description': description})
    return issue.iid

def get_default_branch_name(repository):
    """Determine name of default branch"""
    repo = get_repository_handle(repository)
    return repo.default_branch



def close_issue(repository, issue_number):
    """
    Close an issue in a GitLab repository.

    Parameters
    ----------
    repository : str
        The full name of the GitLab project (e.g., "username/repo-name").
    issue_number : int
        The issue number to close.

    Returns
    -------
    None
    """
    Log().log(f"-> close_issue({repository}, {issue_number})")
    project = get_repository_handle(repository)
    issue = project.issues.get(issue_number)
    issue.state_event = 'close'
    issue.save()
