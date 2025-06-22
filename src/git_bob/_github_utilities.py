# This file contains utility functions using the github API via github-python:
# https://github.com/PyGithub/PyGithub (licensed LGPL3)
#
import os
from functools import lru_cache
from ._logger import Log

@lru_cache(maxsize=1)
def get_repository_handle(repository):
    """
    Get the GitHub repository object.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").

    Returns
    -------
    github.Repository.Repository
        The GitHub repository object.
    """
    from github import Github
    from github.Auth import Token
    access_token = os.getenv('GITHUB_API_KEY')

    # Create a PyGithub instance using the access token
    g = Github(auth=Token(access_token))

    # Get the repository object
    return g.get_repo(repository)


def add_comment_to_issue(repository, issue, comment):
    """
    Add a comment to a specific GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to add a comment to.
    comment : str
        The comment text to add to the issue.
    """
    Log().log(f"-> add_comment_to_issue({repository}, {issue}, ...)")

    repo = get_repository_handle(repository)

    # Get the issue object
    issue_obj = repo.get_issue(issue)

    if len(comment) > 65535:
        print("Comment is too long. Truncated to 65535 characters. This was the full comment:", comment)
        comment = comment[:65535]

    # Add a new comment to the issue
    issue_obj.create_comment(comment)

    print(f"Comment added to issue #{issue} in repository {repository}.")


def get_conversation_on_issue(repository, issue):
    """
    Retrieve the entire conversation (title, body, and comments) of a specific GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to retrieve the conversation for.

    Returns
    -------
    str
        The conversation string containing the issue title, body, and comments.
    """
    Log().log(f"-> get_conversation_on_issue({repository}, {issue})")

    repo = get_repository_handle(repository)

    # Get the issue by number
    issue_obj = repo.get_issue(issue)

    # Get the conversation as a string
    conversation = f"Issue Title: {issue_obj.title}\n\n"
    conversation += f"Issue Body:\n{issue_obj.body}\n\n"

    # Get all comments on the issue
    comments = issue_obj.get_comments()

    # Append each comment to the conversation string
    for comment in comments:
        conversation += f"Comment by {comment.user.login}:\n{comment.body}\n\n"

    return conversation


def get_most_recently_commented_issue(repository):
    """
    Return the issue number of the issue in a repository where the last comment was posted.
    """
    Log().log(f"-> get_most_recently_commented_issue({repository})")
    repo = get_repository_handle(repository)

    most_recent_comment = None
    issue = None

    # Loop through all issues
    for i in repo.get_issues(state="all"):
        comments = i.get_comments()

        # Loop through each comment in the issue
        for comment in comments:
            if most_recent_comment is None or comment.created_at > most_recent_comment.created_at:
                most_recent_comment = comment
                issue = i

    if issue is None:
        raise ValueError("No issue number provided")

    return issue.number


def get_most_recent_comment_on_issue(repository, issue):
    """
    Retrieve the most recent comment on a specific GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to retrieve the most recent comment for.

    Returns
    -------
    tuple
        A tuple containing the username of the commenter and the comment text.
    """
    Log().log(f"-> get_most_recent_comment_on_issue({repository}, {issue})")
    repo = get_repository_handle(repository)


    # Get the issue by number
    issue_obj = repo.get_issue(issue)

    # Get all comments on the issue
    comments = issue_obj.get_comments()

    # return last comment
    comments = list(comments)
    if len(comments) > 0:
        comment = comments[-1]

        user = comment.user.login
        text = comment.body

    else:
        user = issue_obj.user.login
        text = issue_obj.body

    if text is None:
        text = ""

    return user, text


def list_issues(repository: str, state: str = "open") -> dict:
    """
    List all GitHub issues with a defined state on a specified repository.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    state : str, optional
        The issue status: can be "open", "closed", or "all".

    Returns
    -------
    dict
        A dictionary of issues where keys are issue numbers and values are issue titles.
    """
    Log().log(f"-> list_issues({repository}, {state})")

    repo = get_repository_handle(repository)

    # Fetch all issues with the specified state
    issues = repo.get_issues(state=state)

    result = {}
    # Populate issue dictionary
    for issue in issues:
        result[issue.number] = issue.title

    return result


def get_issue_details(repository: str, issue: int) -> str:
    """
    Retrieve detailed information about a specific GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to retrieve details for.

    Returns
    -------
    str
        A string containing detailed information about the issue.
    """
    Log().log(f"-> get_github_issue_details({repository}, {issue})")

    repo = get_repository_handle(repository)

    # Fetch the specified issue
    issue = repo.get_issue(number=issue)

    # Format issue details
    content = f"""
Issue #{issue.number}: {issue.title}
State: {issue.state}
Created at: {issue.created_at}
Updated at: {issue.updated_at}
Closed at: {issue.closed_at}
Author: {issue.user.login}
Assignees: {', '.join([assignee.login for assignee in issue.assignees])}
Labels: {', '.join([label.name for label in issue.labels])}
Comments: {issue.comments}
Body:
{issue.body}
"""

    # Add comments if any
    if issue.comments > 0:
        content += "\n\nComments:"
        comments = issue.get_comments()
        for comment in comments:
            content += f"\n\nComment by {comment.user.login} on {comment.created_at}:\n{comment.body}"

    return content


def list_repository_files(repository: str, branch_name: str = None, file_patterns:list = None) -> list:
    """
    List all files in a given GitHub repository.

    This function uses the GitHub API to retrieve and list all files
    in the specified repository.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str, optional
        The name of the branch or tag (default is 'main').
    file_patterns : list, optional
        A list of file patterns to filter the files by.

    Returns
    -------
    list
        A list of strings, where each string is the path of a file in the repository.
    """
    Log().log(f"-> list_repository_files({repository})")
    if branch_name is None:
        branch_name = get_default_branch_name(repository)

    # Initialize Github client
    repo = get_repository_handle(repository)

    # Get all contents of the repository
    contents = repo.get_contents("", ref=branch_name)

    # List to store all file paths
    all_files = []

    # Iterate through all contents
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            # If it's a directory, get its contents and add them to the list
            contents.extend(repo.get_contents(file_content.path, ref=branch_name))
        else:
            # If it's a file, add its path to the list
            if file_patterns is None or any([f in file_content.path for f in file_patterns]):
                all_files.append(file_content.path)

    return all_files


def get_repository_file_contents(repository: str, branch_name, file_paths: list) -> dict:
    """
    Retrieve the contents of specified files from a GitHub repository.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str, optional
        The name of the branch or tag.
    file_paths : list
        A list of file paths within the repository to retrieve the contents of.

    Returns
    -------
    dict
        A dictionary where keys are file paths and values are the contents of the files.
    """
    Log().log(f"-> get_repository_file_contents({repository}, {branch_name}, {file_paths})")

    # Dictionary to store file contents
    file_contents = {}

    # Iterate through the file paths
    for file_path in file_paths:
        try:
            # Get the file content
            file_content = get_file_in_repository (repository, branch_name, file_path).decoded_content.decode()

            # store the content
            file_contents[file_path] = file_content

        except Exception as e:
            file_contents[file_path] = f"Error accessing {file_path}: {str(e)}"

    return file_contents


def write_file_in_branch(repository, branch_name, file_path, new_content, commit_message="Update file"):
    """
    Modifies or creates a specified file with new content and saves the changes in a new git branch.
    The name of the new branch is returned.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to write the changes to.
    file_path : str
        A file path within the repository to change the contents of.
    new_content : str
        Text content that should be written into the file.
    commit_message : str, optional
        The commit message for the changes. Default is "Update file".

    Returns
    -------
    str
        The name of the branch where the changed file is stored.
    """
    Log().log(f"-> write_file_in_new_branch({repository}, {branch_name}, {file_path}, ...)")

    # Authenticate with GitHub
    repo = get_repository_handle(repository)

    # Commit the changes
    if check_if_file_exists(repository, branch_name, file_path):
        file = get_file_in_repository(repository, branch_name, file_path)
        print("update file", file_path, file.sha)
        repo.update_file(file.path, commit_message, new_content, file.sha, branch=branch_name)
    else:
        print("create file", file_path)
        repo.create_file(file_path, commit_message, new_content, branch=branch_name)

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
    Creates a new branch in a given repository, derived from an optionally specified parent_branch and returns the name of the new branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    parent_branch : str, optional
        The name of the parent branch from which the new branch will be created. Default is "main".

    Returns
    -------
    str
        The name of the newly created branch.
    """
    Log().log(f"-> create_branch({repository}, {parent_branch})")
    if parent_branch is None:
        parent_branch = get_default_branch_name(repository)


    import random
    import string

    # Authenticate with GitHub
    repo = get_repository_handle(repository)

    # Get the main branch
    main_branch = repo.get_branch(parent_branch)

    # Create a new branch
    new_branch_name = "git-bob-mod-" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=main_branch.commit.sha)

    return new_branch_name


def check_if_file_exists(repository, branch_name, file_path):
    """
    Checks if a specified file_path exists in a GitHub repository. Returns True if the file exists, False otherwise.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name: str
        The name of the branch to check the file in.
    file_path : str
        The path of the file to check.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    Log().log(f"-> check_if_file_exists({repository}, {file_path})")
    # Authenticate with GitHub
    #repo = get_github_repository(repository)

    try:
        # Try to get the contents of the file
        get_file_in_repository(repository, branch_name, file_path)
        #contents = repo.get_contents(file_path)
        return True
    except:
        return False


def get_file_in_repository(repository, branch_name, file_path):
    """
    Helper function to prevent multiple calls to the GitHub API for the same file.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to get the file content from.
    file_path : str
        The path of the file in the repository.

    Returns
    -------
    github.ContentFile.ContentFile
        The content file object of the specified file.
    """
    print(f"-> get_file_in_repository({repository}, {branch_name}, {file_path})")
    if file_path.endswith(")"):
        file_path = file_path[:-1]
    if file_path.endswith("'"):
        file_path = file_path[:-1]
    if file_path.endswith('"'):
        file_path = file_path[:-1]

    if file_path.endswith("?raw=true"):
        print("fixing file path")
        file_path = file_path[:-9]

    print("loading file content...", file_path)
    repo = get_repository_handle(repository)
    return repo.get_contents(file_path, ref=branch_name)


def send_pull_request(repository, source_branch, target_branch, title, description):
    """
    Create a pull request from a defined branch into the main branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    source_branch : str
        The name of the branch that should be merged into target_branch.
    target_branch : str
        The name of the branch that the source_branch should be merged into.
    title : str
        A one-liner explaining what was changed in the branch.
    description : str
        A more detailed description of what has happened.
        If the changes are related to an issue write "closes #99 "
        where 99 stands for the issue number the pull-request is related to.

    Returns
    -------
    str
        The URL to the pull-request that was just created.
    """
    Log().log(f"-> send_pull_request({repository}, {source_branch}, {target_branch}, ...)")

    # Authenticate with GitHub
    repo = get_repository_handle(repository)

    if len(description) > 65535:
        print("Description is too long. Truncated to 65535 characters. This was the full description:", description)
        description = description[:65535]

    # Create a pull request
    pr = repo.create_pull(title=title, body=description, head=source_branch, base=target_branch)

    return f"Pull request created: {pr.html_url}"


def check_access_and_ask_for_approval(user, repository, issue):
    """
    Check if the user has access rights and ask for approval if necessary.

    Parameters
    ----------
    user : str
        The username of the person requesting access.
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number related to the access request.

    Returns
    -------
    bool
        True if the user has access rights, False otherwise.
    """
    # Check if the user is a repository member
    Log().log(f"-> check_access_and_ask_for_approval({user}, {repository}, {issue})")
    groups = os.getenv('GIT_BOB_ACCESS_GROUPS', 'members').split(',')

    from ._ai_github_utilities import setup_ai_remark
    access = False

    repo = get_repository_handle(repository)

    members = [member.login for member in repo.get_collaborators()]

    if "members" in groups:
        if user in members:
            access = True
    if "bot" in groups:
        if user == "github-actions[bot]":
            access = True

    if not access:
        print("User does not have access rights.")

        remark = setup_ai_remark()
        agent_name = os.getenv('AGENT_NAME', 'git-bob')

        add_comment_to_issue(repository, issue,f"""
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
    Get the list of contributors to a GitHub repository.
    """
    Log().log(f"-> get_contributors({repository})")
    repo = get_repository_handle(repository)

    return [member.login for member in repo.get_contributors()]


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


def add_reaction_to_issue(repository, issue, reaction="+1"):
    """
    Add a given reaction to a github issue.
    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to add a reaction to.
    reaction : str
        The reaction to add. Default is "+1".
    """
    Log().log(f"-> add_reaction_to_issue({repository}, {issue}, {reaction})")

    repo = get_repository_handle(repository)

    # Fetch the specified issue
    issue = repo.get_issue(number=issue)
    issue.create_reaction(reaction)


def add_reaction_to_last_comment_in_issue(repository, issue, reaction="+1"):
    """
    Add a given reaction to the last comment in a github issue.
    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to add a reaction to.
    reaction : str
        The reaction to add. Default is "+1".
    """
    Log().log(f"-> add_reaction_to_last_comment_in_issue({repository}, {issue}, {reaction})")

    repo = get_repository_handle(repository)

    # Get the issue by number
    issue_obj = repo.get_issue(issue)

    # Get all comments on the issue
    comments = issue_obj.get_comments()

    # return last comment
    comments = list(comments)
    if len(comments) > 0:
        comments[-1].create_reaction(reaction)
    else:
        issue_obj.create_reaction(reaction)


def get_diff_of_branches(repository, compare_branch, base_branch=None):
    """
    Get the diff between two branches in a GitHub repository.
    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    compare_branch : str
        The branch to compare against the base branch.
    base_branch : str, optional
        The base branch to compare against. Default is "main".
    Returns
    -------
    str
        The diff between the specified branches as a string.
    """
    if base_branch is None:
        base_branch = get_default_branch_name(repository)

    # Get the repository
    repo = get_repository_handle(repository)

    # Get the comparison between branches
    comparison = repo.compare(base_branch, compare_branch)
    # Initialize output variable
    output = []
    # Collect the diff
    for file in comparison.files:
        output.append(f"\nFile: {file.filename}")
        output.append(f"Status: {file.status}")
        output.append("-" * 40)
        if file.patch:
            output.append(file.patch)
        else:
            output.append("No diff available (possibly a binary file)")
    return "\n".join(output)


def rename_file_in_repository(repository, branch_name, old_file_path, new_file_path, commit_message="Rename file"):
    """
    Rename a file in the specified GitHub repository on a given branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to rename the file in.
    old_file_path : str
        The current file path.
    new_file_path : str
        The new file path.
    commit_message : str, optional
        The commit message for the rename. Default is "Rename file".

    Returns
    -------
    bool
        True if the file was renamed successfully, False otherwise.
    """
    Log().log(f"-> rename_file_in_repository({repository}, {branch_name}, {old_file_path}, {new_file_path})")

    # Authenticate with GitHub
    repo = get_repository_handle(repository)

    file = get_file_in_repository(repository, branch_name, old_file_path)
    # Create a new file with the old content at the new path
    repo.create_file(new_file_path, commit_message, file.decoded_content.decode(), branch=branch_name)

    # Delete the old file
    repo.delete_file(old_file_path, commit_message, file.sha, branch=branch_name)

    # move file locally using shutil
    import shutil
    shutil.move(old_file_path, new_file_path)


def decode_file(file):
    return file.decoded_content.decode()


def delete_file_from_repository(repository, branch_name, file_path, commit_message="Delete file"):
    """
    Delete a file from the specified GitHub repository on a given branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to delete the file from.
    file_path : str
        The path of the file to delete.
    commit_message : str, optional
        The commit message for the deletion. Default is "Delete file".

    Returns
    -------
    bool
        True if the file was deleted successfully, False otherwise.
    """
    Log().log(f"-> delete_file_in_repository({repository}, {branch_name}, {file_path})")

    # Authenticate with GitHub
    repo = get_repository_handle(repository)

    file = get_file_in_repository(repository, branch_name, file_path)
    repo.delete_file(file.path, commit_message, file.sha, branch=branch_name)


def copy_file_in_repository(repository, branch_name, src_file_path, dest_file_path, commit_message="Copy file"):
    """
    Copy a file in the specified GitHub repository on a given branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to copy the file in.
    src_file_path : str
        The source file path.
    dest_file_path : str
        The destination file path.
    commit_message : str, optional
        The commit message for the copy. Default is "Copy file".

    Returns
    -------
    bool
        True if the file was copied successfully, False otherwise.
    """
    Log().log(f"-> copy_file_in_repository({repository}, {branch_name}, {src_file_path}, {dest_file_path})")

    # Authenticate with GitHub
    repo = get_repository_handle(repository)

    file = get_file_in_repository(repository, branch_name, src_file_path)
    file_content = file.decoded_content.decode()

    # Create a new file with the old content at the new path
    repo.create_file(dest_file_path, commit_message, file_content, branch=branch_name)

    # save the file
    with open(dest_file_path, "w") as f:
        f.write(file_content)


def download_to_repository(repository, branch_name, source_url, target_filename):
    """Download a file from a URL and upload it to a GitHub repository."""
    import requests
    import base64
    from github import Github
    from ._logger import Log
    Log().log(f"-> download_to_repository({repository}, {branch_name}, {source_url}, {target_filename})")

    if not (source_url.startswith("https://github.com") or source_url.startswith("https://raw.githubusercontent.com")):
        raise Exception("Can only download from GitHub URLs or raw GitHub content URLs.")

    if source_url.endswith(")"): # happens with ![]() markdown syntax
        source_url = source_url[:-1]

    # Download the file
    response = requests.get(source_url)
    if response.status_code == 200:
        file_content = response.content
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

    # Upload the file to the GitHub repository using the GitHub API
    repo = get_repository_handle(repository)

    commit_message = f"Downloaded {source_url}, saved as {target_filename}."

    # save the file locally
    with open(target_filename, "wb") as f:
        f.write(file_content)

    # Check if the file already exists
    try:
        contents = repo.get_contents(target_filename)
        # If file exists, we need to update it
        repo.update_file(contents.path, commit_message, file_content, contents.sha, branch=branch_name)
        print(f"File '{target_filename}' successfully updated.")
    except:
        # If file does not exist, create a new one
        repo.create_file(target_filename, commit_message, file_content, branch=branch_name)
        print(f"File '{target_filename}' successfully uploaded.")


def create_issue(repository, title, description):
    """
    Create a new GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    title : str
        The title of the GitHub issue.
    description : str
        The detailed description of the GitHub issue.

    Returns
    -------
    int
        The number of the created issue.
    """
    Log().log(f"-> create_issue({repository}, {title})")
    repo = get_repository_handle(repository)

    print("repo", repo)

    # Create a new issue
    issue_obj = repo.create_issue(title=title, body=description)

    print(f"Issue created: #{issue_obj.number}")
    return issue_obj.number


def get_default_branch_name(repository):
    """Determine name of default branch"""
    repo = get_repository_handle(repository)
    return repo.get_branch(repo.default_branch).name


def close_issue(repository, issue_number):
    """
    Close a GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue_number : int
        The number of the issue to close.
    """
    Log().log(f"-> close_issue({repository}, {issue_number})")
    repo = get_repository_handle(repository)

    # Get the issue by number
    issue_obj = repo.get_issue(issue_number)

    # Close the issue
    issue_obj.edit(state="closed")
