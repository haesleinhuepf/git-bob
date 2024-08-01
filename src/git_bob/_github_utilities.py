import os
from github import Github

def comment_on_issue(repository, issue, comment):
    """Add a comment to a specified GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to comment on.
    comment : str
        The comment text to add to the issue.

    Returns
    -------
    None
    """
    print(f"-> comment_on_issue({repository}, {issue}, ...)")

    access_token = os.getenv('GITHUB_API_KEY')

    # Create a PyGithub instance using the access token
    g = Github(access_token)

    # Get the repository object
    repo = g.get_repo(repository)

    # Get the issue object
    issue_obj = repo.get_issue(issue)

    # Add a new comment to the issue
    issue_obj.create_comment(comment)

    print(f"Comment added to issue #{issue} in repository {repository}.")


def get_conversation_on_issue(repository, issue):
    """Retrieve the conversation (title, body, and comments) of a specified GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to retrieve the conversation for.

    Returns
    -------
    str
        The conversation details as a formatted string.
    """
    print(f"-> get_conversation_on_issue({repository}, {issue})")

    access_token = os.getenv('GITHUB_API_KEY')
    g = Github(access_token)

    # Get the repository
    repo = g.get_repo(repository)

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
    """Retrieve the most recent comment on a specified GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to retrieve the most recent comment for.

    Returns
    -------
    tuple
        A tuple containing the username and the text of the most recent comment.
    """
    print(f"-> get_most_recent_comment_on_issue({repository}, {issue})")

    access_token = os.getenv('GITHUB_API_KEY')
    g = Github(access_token)

    # Get the repository
    repo = g.get_repo(repository)

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
    """List all GitHub issues with a defined state on a specified repository.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    state : str, optional
        The issue status: can be "open", "closed", or "all". Default is "open".

    Returns
    -------
    dict
        A dictionary of issues with issue numbers as keys and titles as values.
    """
    print(f"-> list_issues({repository}, {state})")

    from github import Github

    # Initialize Github client
    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
    g = Github(GITHUB_API_KEY)

    # Get the repository
    repo = g.get_repo(repository)

    # Fetch all open issues
    issues = repo.get_issues(state=state)

    result = {}
    # Print open issues
    for issue in issues:
        result[issue.number] = issue.title

    return result


def get_github_issue_details(repository: str, issue: int) -> str:
    """Retrieve detailed information about a specific GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to retrieve details for.

    Returns
    -------
    str
        A formatted string containing detailed information about the issue.
    """
    print(f"-> get_github_issue_details({repository}, {issue})")

    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
    g = Github(GITHUB_API_KEY)

    # Get the repository
    repo = g.get_repo(repository)

    # Fetch the specified issue
    issue = repo.get_issue(number=issue)

    # Format issue details
    content = f"""Issue #{issue.number}: {issue.title}
State: {issue.state}
Created at: {issue.created_at}
Updated at: {issue.updated_at}
Closed at: {issue.closed_at}
Author: {issue.user.login}
Assignees: {', '.join([assignee.login for assignee in issue.assignees])}
Labels: {', '.join([label.name for label in issue.labels])}
Comments: {issue.comments}
Body:
{issue.body}"""

    # Add comments if any
    if issue.comments > 0:
        content += "\n\nComments:"
        comments = issue.get_comments()
        for comment in comments:
            content += f"\n\nComment by {comment.user.login} on {comment.created_at}:\n{comment.body}"

    return content


def list_repository_files(repo_name: str) -> list:
    """List all files in a given GitHub repository.

    This function uses the GitHub API to retrieve and list all files
    in the specified repository.

    Parameters
    ----------
    repo_name : str
        The full name of the GitHub repository (e.g., "username/repo-name").

    Returns
    -------
    list
        A list of strings, where each string is the path of a file in the repository.
    """
    print(f"-> list_repository_files({repo_name})")

    from github import Github

    # Initialize Github client
    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
    g = Github(GITHUB_API_KEY)

    # Get the repository
    repo = g.get_repo(repo_name)

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


def get_repository_file_contents(repo_name: str, file_paths: list) -> dict:
    """Retrieve the contents of specified files from a GitHub repository.

    Parameters
    ----------
    repo_name : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    file_paths : list
        A list of file paths within the repository to retrieve the contents of.

    Returns
    -------
    dict
        A dictionary where keys are file paths and values are the contents of the files.
    """
    print(f"-> get_repository_file_contents({repo_name}, {file_paths})")

    from github import Github

    # Initialize Github client
    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
    g = Github(GITHUB_API_KEY)

    # Get the repository
    repo = g.get_repo(repo_name)

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


def update_file_in_new_branch(repository, file_path, new_content):
    """Modifies a specified file with new content and saves the changes in a new git branch.
    The name of the new branch is returned.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    file_path : str
        A file path within the repository to change the contents of.
    new_content : str
        Text content that should be written into the file.

    Returns
    -------
    str
        The name of the branch where the changed file is stored.
    """
    print(f"-> update_file_in_new_branch({repository}, {file_path}, ...)")

    from github import Github
    import os
    import random
    import string

    # Authenticate with GitHub
    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
    g = Github(GITHUB_API_KEY)

    # Get the repository
    repo = g.get_repo(repository)

    # Get the main branch
    main_branch = repo.get_branch("main")

    # Access the file
    file = repo.get_contents(file_path)

    # Create a new branch
    new_branch_name = "mod-" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=main_branch.commit.sha)

    # Commit the changes
    repo.update_file(file.path, "Update file content", new_content, file.sha, branch=new_branch_name)

    return new_branch_name


def send_pull_request(repository, branch_name, title, description):
    """Create a pull request from a defined branch into the main branch.

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

    from github import Github
    import os

    # Authenticate with GitHub
    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
    g = Github(GITHUB_API_KEY)

    # Get the repository
    repo = g.get_repo(repository)

    # Create a pull request
    remark = "<sup>This comment was generated by [git-bob](https://github.com/haesleinhuepf/git-bob), an AI-based assistant.</sup>\n\n"
    pr = repo.create_pull(title=title, body=remark + description, head=branch_name, base="main")

    return f"Pull request created: {pr.html_url}"


def solve_github_issue(repository, issue):
    """Attempt to solve a GitHub issue by modifying a single file and sending a pull-request.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The issue number to solve.

    Returns
    -------
    None
    """
    print(f"-> solve_github_issue({repository}, {issue})")
    from blablado import Assistant
    assistant = Assistant()
    assistant.register_tool(get_github_issue_details)
    assistant.register_tool(list_repository_files)
    assistant.register_tool(get_repository_file_contents)
    assistant.register_tool(update_file_in_new_branch)
    assistant.register_tool(send_pull_request)

    assistant.do(f"Tell me the most important details of issue #{issue} in the repository {repository}")
    assistant.do(f"List all files in the repository {repository}")
    filename = assistant.tell("Which of these files might be relevant for issue #{issue} ? Respond ONLY the filename.")
    print("Related filename", filename)
    assistant.do(f"Load the entire content of {filename} from the repository {repository} .")
    assistant.do(f"Modify the file content of {filename} to fix the issue in a new branch.")
    assistant.do("Send a pull-request of the new branch explaining what we changed.")
