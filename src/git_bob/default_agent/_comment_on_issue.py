def comment_on_issue(repository, issue, prompt_function, **kwargs):
    """
    Comment on a GitHub issue using a prompt function.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository.
    issue : int
        The issue number to comment on.
    prompt_function : function
        The function to generate the comment.
    """
    from .._logger import Log
    from .._utilities import text_to_json, modify_discussion, clean_output, redact_text, Config, SYSTEM_PROMPT, setup_ai_remark
    Log().log(f"-> comment_on_issue({repository}, {issue})")

    if Config.pull_request is not None:
        file_changes = "\n## Changed files\n\n" + Config.git_utilities.get_diff_of_pull_request(repository, issue) + "\n\n"
        print("file_changes:", file_changes)
        conversation_type = "pull-request"
    else:
        file_changes = ""
        conversation_type = "issue"

    discussion = modify_discussion(Config.git_utilities.get_conversation_on_issue(repository, issue), prompt_visionlm=prompt_function)
    print("Discussion:", discussion)

    all_files = "* " + "\n* ".join(Config.git_utilities.list_repository_files(repository))

    relevant_files = prompt_function(f"""
{SYSTEM_PROMPT}
Decide what to do to respond to a github {conversation_type}. The entire discussion is given and a list of all files in the repository.

## Discussion of the issue #{issue}

{discussion}
{file_changes}
## All files in the repository

{all_files}

## Your task
Which of these files are necessary to read for solving the issue #{issue} ? Keep the list short.
Returning an empty list is also a valid answer.
Respond with the filenames as JSON list.
""")
    filenames = text_to_json(relevant_files)

    file_content_dict = Config.git_utilities.get_repository_file_contents(repository, "main", filenames)

    temp = []
    for k, v in file_content_dict.items():
        temp = temp + [f"### File {k} content\n\n```\n{v}\n```\n"]
    relevant_files_contents = "\n".join(temp)

    comment = prompt_function(f"""
{SYSTEM_PROMPT}
Respond to a github {conversation_type}. Its entire discussion is given and additionally, content of some relevant files.

## Discussion

{discussion}
{file_changes}
## Relevant files

{relevant_files_contents}

## Your task

Respond to the discussion above as if you were a human talking to a human.
In case code-changes are discussed, make a proposal of how new code could look like.
Do NOT explain your response. Just explain code shortly if you are responding with code. 
Do not repeat answers that were given already.
Focus on the most recent discussion.
Just respond to the discussion.
""")
    comment = redact_text(clean_output(repository, comment))

    print("comment:", comment)

    comment = comment.strip("\n").strip().strip("\n")

    if comment.startswith("from ") or comment.startswith("import "):
        comment = "```python\n" + comment + "\n```"

    ai_remark = setup_ai_remark()
    Config.git_utilities.add_comment_to_issue(repository, issue, f"""        
{ai_remark}

{comment}
""")