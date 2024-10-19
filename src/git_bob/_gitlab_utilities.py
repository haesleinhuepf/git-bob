import os
from gitlab import Gitlab

def get_gitlab_repository(repository):
    """
    Get the GitLab repository object using an API token from environment.
    
    Parameters
    ----------
    repository : str
        The repository identifier, typically in the format 'owner/repo'.
    
    Returns
    -------
    gitlab.v4.objects.Project
        An object representing the GitLab project.
    """
    gitlab_url = os.getenv('GITLAB_URL', 'https://gitlab.com')
    private_token = os.environ['GITLAB_API_KEY']
    gl = Gitlab(gitlab_url, private_token=private_token)
    return gl.projects.get(repository)

def check_if_file_exists(repository, branch_name, file_path):
    """
    Check if a file exists in a given branch of the GitLab repository.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    branch_name : str
        The branch name to check the file existence.
    file_path : str
        The path to the file in the repository.
    
    Returns
    -------
    bool
        True if the file exists, otherwise False.
    """
    repo = get_gitlab_repository(repository)
    try:
        repo.files.get(file_path=file_path, ref=branch_name)
        return True
    except:
        return False

def write_file_in_branch(repository, branch_name, file_path, new_content, commit_message):
    """
    Write or update a file in a specified branch of a GitLab repository.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    branch_name : str
        The branch name where the file will be written.
    file_path : str
        The path to the file in the repository.
    new_content : str
        The new content to be written to the file.
    commit_message : str
        The commit message for the file update.
    """
    repo = get_gitlab_repository(repository)
    try:
        file_obj = repo.files.get(file_path=file_path, ref=branch_name)
        file_obj.content = new_content
        file_obj.save(branch=branch_name, commit_message=commit_message)
    except:
        repo.files.create({
            'file_path': file_path,
            'branch': branch_name,
            'content': new_content,
            'encoding': 'base64',
            'commit_message': commit_message
        })

def check_access_and_ask_for_approval(user, repository, issue):
    """
    Check user access in the repository and potentially ask for approval via issuing a comment.
    
    Parameters
    ----------
    user : str
        The username to check access for.
    repository : str
        The repository identifier.
    issue : int
        The issue number to interact with if approval is needed.
    
    Returns
    -------
    bool
        True if access is granted, otherwise False.
    """
    repo = get_gitlab_repository(repository)
    access = False

    try:
        member = repo.members.get(user)
        access = True if member.access_level >= 30 else False
    except:
        access = False

    if not access:
        issue_obj = repo.issues.get(issue)
        issue_obj.notes.create({'body': f"User {user} needs approval for access."})

    return access

def get_gitlab_issue_details(repository, issue):
    """
    Get the details of a specific issue in a GitLab repository.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    issue : int
        The issue number.
    
    Returns
    -------
    str
        A formatted string with issue details.
    """
    repo = get_gitlab_repository(repository)
    issue_obj = repo.issues.get(issue)
    return f"Issue #{issue_obj.iid}: {issue_obj.title}\nDetails:\n{issue_obj.description}"

def get_contributors(repository):
    """
    Get the list of contributors to a GitLab repository.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    
    Returns
    -------
    list
        A list of usernames who are contributors.
    """
    repo = get_gitlab_repository(repository)
    return [member.username for member in repo.repository_contributors()]

def get_conversation_on_issue(repository, issue):
    """
    Retrieve the conversation on a specific issue including comments.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    issue : int
        The issue number.
    
    Returns
    -------
    str
        The complete conversation thread on the issue.
    """
    repo = get_gitlab_repository(repository)
    issue_obj = repo.issues.get(issue)
    conversation = f"Issue Title: {issue_obj.title}\n\nIssue Body:\n{issue_obj.description}\n\n"
    comments = issue_obj.notes.list()
    for comment in comments:
        conversation += f"Comment by {comment.author['username']}:\n{comment.body}\n\n"
    return conversation

def get_diff_of_pull_request(repository, mergerequest_id):
    """
    Get the diff of a specific merge request.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    mergerequest_id : int
        The merge request ID.
    
    Returns
    -------
    list
        A list of diffs in the merge request.
    """
    repo = get_gitlab_repository(repository)
    mr = repo.mergerequests.get(mergerequest_id)
    return mr.diffs()

def create_branch(repository, branch_name, ref_branch='main'):
    """
    Create a new branch from a reference branch in a GitLab repository.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    branch_name : str
        The name of the branch to be created.
    ref_branch : str, optional
        The reference branch to create the new branch from, by default 'main'.
    
    Returns
    -------
    str
        The name of the created branch.
    """
    repo = get_gitlab_repository(repository)
    branch = repo.branches.create({'branch': branch_name, 'ref': ref_branch})
    return branch.name

def get_diff_of_branches(repository, source_branch, target_branch):
    """
    Get the diff between two branches.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    source_branch : str
        The source branch name.
    target_branch : str
        The target branch name.
    
    Returns
    -------
    list
        A list of diffs between the two branches.
    """
    repo = get_gitlab_repository(repository)
    return repo.repository_compare(source_branch, target_branch)

def add_reaction_to_last_comment_in_issue(repository, issue, reaction):
    """
    Add a reaction to the last comment on a specific issue.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    issue : int
        The issue number.
    reaction : str
        The reaction emoji name.
    """
    repo = get_gitlab_repository(repository)
    issue_obj = repo.issues.get(issue)
    comments = issue_obj.notes.list(order_by='created_at', sort='desc')
    if comments:
        comments[0].award_emoji.create({'name': reaction})

def add_reaction_to_issue(repository, issue, reaction):
    """
    Add a reaction to an issue.
    
    Parameters
    ----------
    repository : str
        The repository identifier.
    issue : int
        The issue number.
    reaction : str
        The reaction emoji name.
    """
    repo = get_gitlab_repository(repository)
    issue_obj = repo.issues.get(issue)
    issue_obj.award_emoji.create({'name': reaction})
