import os
import requests

def get_github_issue_details(repository, issue):
    """Retrieve detailed information about a specific GitHub issue."""
    url = f"https://api.github.com/repos/{repository}/issues/{issue}"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(url, headers=headers)
    return response.json()

def list_repository_files(repo_name):
    """List all files in a given GitHub repository."""
    url = f"https://api.github.com/repos/{repo_name}/git/trees/main?recursive=1"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(url, headers=headers)
    return [file['path'] for file in response.json().get('tree', [])]

def get_repository_file_contents(repo_name, file_paths):
    """Retrieve the contents of specified files from a GitHub repository."""
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    contents = {}
    for path in file_paths:
        url = f"https://api.github.com/repos/{repo_name}/contents/{path}"
        response = requests.get(url, headers=headers)
        contents[path] = response.json().get('content', '')
    return contents

def write_file_in_new_branch(repository, branch_name, file_path, new_content):
    """Modifies or creates a specified file with new content and saves the changes in a new git branch."""
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
    data = {
        "message": f"Update {file_path}",
        "content": new_content,
        "branch": branch_name
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def send_pull_request(repository, branch_name, title, description):
    """Create a pull request from a defined branch into the main branch."""
    url = f"https://api.github.com/repos/{repository}/pulls"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    data = {
        "title": title,
        "body": description,
        "head": branch_name,
        "base": "main"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json().get('html_url')

def get_conversation_on_issue(repository, issue):
    """Retrieve the conversation on a specific GitHub issue."""
    url = f"https://api.github.com/repos/{repository}/issues/{issue}/comments"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(url, headers=headers)
    return response.json()

def add_comment_to_issue(repository, issue, comment):
    """Add a comment to a specific GitHub issue."""
    url = f"https://api.github.com/repos/{repository}/issues/{issue}/comments"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_diff_of_pull_request(repository, issue):
    """Retrieve the diff of a specific pull request."""
    url = f"https://api.github.com/repos/{repository}/pulls/{issue}/files"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(url, headers=headers)
    return response.json()

def create_branch(repository, parent_branch="main"):
    """Creates a new branch in a given repository, derived from an optionally specified parent_branch."""
    url = f"https://api.github.com/repos/{repository}/git/refs/heads/{parent_branch}"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(url, headers=headers)
    sha = response.json().get('object', {}).get('sha')
    new_branch = f"mod-{sha[:7]}"
    data = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }
    url = f"https://api.github.com/repos/{repository}/git/refs"
    response = requests.post(url, headers=headers, json=data)
    return new_branch

def check_if_file_exists(repository, file_path):
    """Check if a file exists in the given repository."""
    url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(url, headers=headers)
    return response.status_code == 200
