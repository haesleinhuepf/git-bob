# This file contains utility functions using the github API via github-python:
# https://github.com/PyGithub/PyGithub (licensed LGPL3)
#
# All functions must have a proper docstring, because we are using them as tools for function calling using LLMs.
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def get_github_repository(repository):
    from github import Github
    access_token = os.getenv('GITHUB_API_KEY')

    # Create a PyGithub instance using the access token
    g = Github(access_token)

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
    print(f"-> add_comment_to_issue({repository}, {issue}, ...)")
    repo = get_github_repository(repository)

    # Get the issue object
    issue_obj = repo.get_issue(issue)

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
    print(f"-> get_conversation_on_issue({repository}, {issue})")

    repo = get_github_repository(repository)

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
    print(f"-> get_most_recent_comment_on_issue({repository}, {issue})")

    repo = get_github_repository(repository)

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
    print(f"-> list_issues({repository}, {state})")

    repo = get_github_repository(repository)

    # Fetch all open issues
    issues = repo.get_issues(state=state)

    result = {}
    # Print open issues
    for issue in issues:
        result[issue.number] = issue.title

    return result


def get_github_issue_details(repository: str, issue: int) -> str:
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
    from ._utilities import remove_indentation
    print(f"-> get_github_issue_details({repository}, {issue})")

    repo = get_github_repository(repository)

    # Fetch the specified issue
    issue = repo.get_issue(number=issue)

    # Format issue details
    content = remove_indentation(f"""Issue #{issue.number}: {issue.title}
    State: {issue.state}
    Created at: {issue.created_at}
    Updated at: {issue.updated_at}
    Closed at: {issue.closed_at}
    Author: {issue.user.login}
    Assignees: {', '.join([assignee.login for assignee in issue.assignees])}
    Labels: {', '.join([label.name for label in issue.labels])}
    Comments: {issue.comments}
    Body:
    {issue.body}""")

    # Add comments if any
    if issue.comments > 0:
        content += "\n\nComments:"
        comments = issue.get_comments()
        for comment in comments:
            content += f"\n\nComment by {comment.user.login} on {comment.created_at}:\n{comment.body}"

    return content


def list_repository_files(repository: str) -> list:
    """
    List all files in a given GitHub repository.

    This function uses the GitHub API to retrieve and list all files
    in the specified repository.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").

    Returns
    -------
    list
        A list of strings, where each string is the path of a file in the repository.
    """
    print(f"-> list_repository_files({repository})")

    # Initialize Github client
    repo = get_github_repository(repository)

    # Get all contents of the repository
    contents = repo.get_contents("")

    # List to store all file paths
    all_files = []

    # Iterate through all contents
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            # If it's a directory, get its contents and add them to the list
            contents.extend(repo.get_contents(file_content.path))
        else:
            # If it's a file, add its path to the list
            all_files.append(file_content.path)

    return all_files


def get_repository_file_contents(repository: str, file_paths: list) -> dict:
    """
    Retrieve the contents of specified files from a GitHub repository.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    file_paths : list
        A list of file paths within the repository to retrieve the contents of.

    Returns
    -------
    dict
        A dictionary where keys are file paths and values are the contents of the files.
    """
    print(f"-> get_repository_file_contents({repository}, {file_paths})")

    # Initialize Github client
    repo = get_github_repository(repository)

    # Dictionary to store file contents
    file_contents = {}

    # Iterate through the file paths
    for file_path in file_paths:
        try:
            # Get the file content
            file_content = repo.get_contents(file_path)

            # Decode and store the content
            file_contents[file_path] = file_content.decoded_content.decode()

        except Exception as e:
            file_contents[file_path] = f"Error accessing {file_path}: {str(e)}"

    return file_contents


def write_file_in_new_branch(repository, branch_name, file_path, new_content):
    """
    Modifies or creates a specified file with new content and saves the changes in a new git branch.
    The name of the new branch is returned.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    file_paths : str
        A file path within the repository to change the contents of.
    new_conent : str
        Text content that should be written into the file.

    Returns
    -------
    str
        The name of the branch where the changed file is stored.
    """
    print(f"-> write_file_in_new_branch({repository}, {branch_name}, {file_path}, ...)")
    import os
    import string

    # print(f'update_file_in_new_branch(repository="{repository}", file_path="{file_path}", new_content="{new_content}")

    # Authenticate with GitHub
    repo = get_github_repository(repository)

    # Commit the changes
    if check_if_file_exists(repository, file_path):
        file = repo.get_contents(file_path, ref=branch_name)
        repo.update_file(file.path, "Update file content", new_content, file.sha, branch=branch_name)
    else:
        repo.create_file(file_path, "Create file content", new_content, branch=branch_name)

    return f"File {file_path} successfully created in repository {repository} branch {branch_name}."

def create_branch(repository, parent_branch="main"):
    """Creates a new branch in a given repository, derived from an optionally specified parent_branch and returns the name of the new branch."""
    print(f"-> create_branch({repository}, {parent_branch})")

    import random
    import string

    # Authenticate with GitHub
    repo = get_github_repository(repository)

    # Get the main branch
    main_branch = repo.get_branch(parent_branch)

    # Create a new branch
    new_branch_name = "mod-" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=main_branch.commit.sha)

    return new_branch_name


def check_if_file_exists(repository, file_path):
    """Checks if a specified file_path exists in a GitHub repository. Returns True if the file exists, False otherwise."""

    print(f"-> check_if_file_exists({repository}, {file_path})")
    # Authenticate with GitHub
    repo = get_github_repository(repository)

    try:
        # Try to get the contents of the file
        contents = repo.get_contents(file_path)
        return True
    except:
        return False


def send_pull_request(repository, branch_name, title, description):
    """
    Create a pull request from a defined branch into the main branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch that should be merged into main.
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
    print(f"-> send_pull_request({repository}, {branch_name}, ...)")

    from ._ai_github_utilities import setup_ai_remark

    # Authenticate with GitHub
    repo = get_github_repository(repository)

    # Create a pull request
    remark = setup_ai_remark() + "\n\n"
    pr = repo.create_pull(title=title, body=remark + description, head=branch_name, base="main")

    return f"Pull request created: {pr.html_url}"


def check_access_and_ask_for_approval(user, repository, issue):
    # Check if the user is a repository member
    print(f"-> check_access_and_ask_for_approval({user}, {repository}, {issue})")

    from ._utilities import remove_indentation
    from ._ai_github_utilities import setup_ai_remark

    repo = get_github_repository(repository)

    members = [member.login for member in repo.get_collaborators()]
    remark = setup_ai_remark()
    if user not in members:
        print("User does not have access rights.")
        member_names = ", ".join(["@" + str(m) for m in members])
        add_comment_to_issue(repository, issue, remove_indentation(remove_indentation(f"""{remark}
                
        Hi @{user}, 
        
        thanks for reaching out! Unfortunately, I'm not allowed to respond to you directly. 
        I need approval from a repository member: {member_names}
        
        Best,
        git-bob
        """)))
        return False
    return True


def get_diff_of_pull_request(repository, pull_request):
    """Get the diff of a specific pull request in a GitHub repository."""
    import requests

    print(f"-> get_diff_of_pull_request({repository}, {pull_request})")
    # Authenticate with GitHub
    repo = get_github_repository(repository)

    pull_request = repo.get_pull(pull_request)

    print(pull_request.diff_url)

    # read the content of a url
    return requests.get(pull_request.diff_url)

