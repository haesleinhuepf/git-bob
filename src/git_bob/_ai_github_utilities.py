from github import Github
import os
from git_bob._config import CONFIG
from git_bob._openai_utilities import get_openai_response

def get_issue_summary(repo_name, issue_number):
    """
    Retrieve a summary of a GitHub issue.

    Parameters
    ----------
    repo_name : str
        The name of the GitHub repository.
    issue_number : int
        The number of the issue to summarize.

    Returns
    -------
    str
        A summary of the GitHub issue.
    """
    g = Github(os.environ.get("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    
    summary = f"Summary of Issue #{issue_number} in {repo_name} repository:\n\n"
    summary += f"Title: {issue.title}\n\n"
    summary += "Key points:\n"
    summary += f"{issue.body}\n"
    
    return summary

def get_file_content(repo_name, file_path):
    """
    Retrieve the content of a file from a GitHub repository.

    Parameters
    ----------
    repo_name : str
        The name of the GitHub repository.
    file_path : str
        The path to the file in the repository.

    Returns
    -------
    str
        The content of the specified file.
    """
    g = Github(os.environ.get("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)
    file_content = repo.get_contents(file_path)
    return file_content.decoded_content.decode()

def update_file_content(repo_name, file_path, content, commit_message):
    """
    Update the content of a file in a GitHub repository.

    Parameters
    ----------
    repo_name : str
        The name of the GitHub repository.
    file_path : str
        The path to the file in the repository.
    content : str
        The new content to be written to the file.
    commit_message : str
        The commit message for the update.

    Returns
    -------
    bool
        True if the update was successful, False otherwise.
    """
    g = Github(os.environ.get("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, commit_message, content, contents.sha)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def solve_issue(repo_name, issue_number):
    """
    Attempt to solve a GitHub issue using OpenAI's API.

    Parameters
    ----------
    repo_name : str
        The name of the GitHub repository.
    issue_number : int
        The number of the issue to solve.

    Returns
    -------
    str
        The solution provided by OpenAI's API.
    """
    issue_summary = get_issue_summary(repo_name, issue_number)
    
    prompt = f"""You are an extremely skilled python developer. Your name is git-bob. 
    You can solve programming tasks and review code.
    When asked to solve a specific problem, you keep your code changes minimal and only solve the problem at hand.
    You cannot execute code. 
    You cannot retrieve information from other sources. 
    Do not claim anything that you don't know.
    In case you are asked to review code, you focus on the quality of the code. 
    
    Given a github issue summary (#{issue_number}) and optionally file content (filename src/git_bob/_ai_github_utilities.py), modify the file content or create the file content to solve the issue.
    
    ## Issue {issue_number} Summary
    
    {issue_summary}
    
    ## File src/git_bob/_ai_github_utilities.py
    Modify the file "src/git_bob/_ai_github_utilities.py" to solve the issue #{issue_number}.
    Keep your modifications absolutely minimal.
    
    That's the file "src/git_bob/_ai_github_utilities.py" content you will find in the file:
    
    
    ## Your task
    Generate content of file "src/git_bob/_ai_github_utilities.py" to solve the issue above.
    Keep your modifications absolutely minimal.
    Respond ONLY the content of the file and afterwards a single line summarizing the changes you made (without mentioning the issue).
    """
    
    return get_openai_response(prompt, CONFIG["OPENAI_MODEL"])