import os
from gitlab import Gitlab

def get_gitlab_repository(repository, private_token):
    gitlab_url = os.getenv('GITLAB_URL', 'https://gitlab.com')
    gl = Gitlab(gitlab_url, private_token=private_token)
    return gl.projects.get(repository)

def check_if_file_exists(repository, branch_name, file_path, private_token):
    """Check if a file exists in the given GitLab repository branch."""
    repo = get_gitlab_repository(repository, private_token)
    try:
        repo.files.get(file_path=file_path, ref=branch_name)
        return True
    except:
        return False

def write_file_in_branch(repository, branch_name, file_path, content, commit_message, private_token):
    """Write a file to a specified branch in a GitLab repository."""
    repo = get_gitlab_repository(repository, private_token)
    repo.files.create({
        'file_path': file_path,
        'branch': branch_name,
        'content': content,
        'commit_message': commit_message
    })

def check_access_and_ask_for_approval(repository, user, private_token):
    """Check if user has access to the repository and request approval."""
    repo = get_gitlab_repository(repository, private_token)
    members = repo.members.all()
    has_access = next((m for m in members if m['username'] == user), None)
    if not has_access:
        raise Exception("User has no access to the repository. Approval needed.")

def get_gitlab_issue_details(repository, issue, private_token):
    """Retrieve details of a GitLab issue."""
    repo = get_gitlab_repository(repository, private_token)
    issue_obj = repo.issues.get(issue)
    return {'title': issue_obj.title, 'description': issue_obj.description}

def get_contributors(repository, private_token):
    """Get list of contributors to the GitLab repository."""
    repo = get_gitlab_repository(repository, private_token)
    return [member.username for member in repo.members.all()]

def get_conversation_on_issue(repository, issue, private_token):
    """Retrieve the conversation of a GitLab issue including all comments."""
    repo = get_gitlab_repository(repository, private_token)
    issue_obj = repo.issues.get(issue)
    conversation = [f"Title: {issue_obj.title}", f"Description: {issue_obj.description}"]
    for note in issue_obj.notes.list():
        conversation.append(f"{note.author['username']}: {note.body}")
    return conversation

def get_diff_of_pull_request(repository, merge_request_id, private_token):
    """Get the diff of a specific GitLab merge request."""
    repo = get_gitlab_repository(repository, private_token)
    mr = repo.mergerequests.get(merge_request_id)
    return mr.changes()['changes']

def create_branch(repository, source_branch, new_branch_name, private_token):
    """Create a new branch in a GitLab repository from an existing branch."""
    repo = get_gitlab_repository(repository, private_token)
    repo.branches.create({'branch': new_branch_name, 'ref': source_branch})

def get_diff_of_branches(repository, source_branch, target_branch, private_token):
    """Get the diff between two branches in a GitLab repository."""
    repo = get_gitlab_repository(repository, private_token)
    return repo.repository_compare(from_=source_branch, to=target_branch)['diff']

def add_reaction_to_last_comment_in_issue(repository, issue, reaction, private_token):
    """Add a reaction to the last comment in a GitLab issue."""
    repo = get_gitlab_repository(repository, private_token)
    issue_obj = repo.issues.get(issue)
    last_note = issue_obj.notes.list(order_by='created_at', sort='desc')[0]
    repo.notes_award.create({'note_id': last_note.id, 'award_emoji': reaction})

def add_reaction_to_issue(repository, issue, reaction, private_token):
    """Add a reaction to the GitLab issue itself."""
    repo = get_gitlab_repository(repository, private_token)
    issue_obj = repo.issues.get(issue)
    issue_obj.award_emoji.create({'name': reaction})
