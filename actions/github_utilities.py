from github import Github

def comment_on_issue(repository, issue, comment):
    # Replace 'YOUR_ACCESS_TOKEN' with your actual GitHub access token
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
    # Create a Github instance using your access token
    from github import Github

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
