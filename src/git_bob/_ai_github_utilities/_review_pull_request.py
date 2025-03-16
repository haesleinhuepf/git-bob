def review_pull_request(repository, issue, prompt_function, **kwargs):
    """
    Review a GitHub pull request using a prompt function.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository.
    issue : int
        The pull request number to review.
    prompt_function : function
        The function to generate the review comment.
    """
    from .._utilities import modify_discussion, clean_output, redact_text, Config, SYSTEM_PROMPT, setup_ai_remark
    from ._comment_on_issue import comment_on_issue
    from .._logger import Log
    Log().log(f"-> review_pull_request({repository}, {issue})")

    if Config.pull_request is None: # it's not a PR
        return comment_on_issue(repository, issue, prompt_function)

    discussion = modify_discussion(Config.git_utilities.get_conversation_on_issue(repository, issue), prompt_visionlm=prompt_function)
    print("Discussion:", discussion)

    file_changes = Config.git_utilities.get_diff_of_pull_request(repository, issue)

    print("file_changes:", file_changes)

    comment = prompt_function(f"""
{SYSTEM_PROMPT}
Generate a response to a github pull-request. 
Given are the discussion on the pull-request and the changed files.
Check if the discussion reflects what was changed in the files.

## Discussion

{discussion}

## Changed files

{file_changes}

## Your task

Review this pull-request and contribute to the discussion as if you were a human talking to a human. 
Respond as if you were a human talking to a human.

Do NOT explain your response or anything else. 
Just respond to the discussion.
""")
    comment = redact_text(clean_output(repository, comment))

    print("comment:", comment)

    ai_remark = setup_ai_remark()
    Config.git_utilities.add_comment_to_issue(repository, issue, f"""        
{ai_remark}

{comment}
""")