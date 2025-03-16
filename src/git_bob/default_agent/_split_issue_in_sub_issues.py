def split_issue_in_sub_issues(repository, issue, prompt_function, base_branch=None):
    """
    Split a main issue into sub-issues for each sub-task.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The main issue number.
    prompt_function : function
        The function to handle prompts.
    base_branch: str
        obsolete and just kept for compatibility reasons
    """
    from .._utilities import text_to_json, Config, setup_ai_remark, SYSTEM_PROMPT, AGENT_NAME
    from .._logger import Log
    Log().log(f"-> split_issue_in_sub_issues({repository}, {issue},...)")

    discussion = Config.git_utilities.get_conversation_on_issue(repository, issue)
    ai_remark = setup_ai_remark()+ "\n"

    # Implement the prompt to parse the discussion
    sub_tasks_json = prompt_function(f"""
{SYSTEM_PROMPT}
You need to extract sub-tasks from a given discussion.
Hint: Sub-tasks are never about "Create an issue for X", but "X" instead. Also sub-tasks are never about "Propose X", but "X" instead.
Return a JSON list with a short title for each sub-task.

## Discussion
{discussion}

## Your task
Extract and return sub-tasks as a JSON list of sub-task titles.
""")

    sub_tasks = text_to_json(sub_tasks_json)
    created_sub_tasks = ""

    sub_issue_numbers = []
    for title in sub_tasks:
        body = prompt_function(f"""
{SYSTEM_PROMPT}
Given description of a list of sub-tasks and extra details given in a discussion, 
extract relevant information for one of the sub-tasks.

## Discussion
{discussion}

{created_sub_tasks}

## Your task
Extract relevant information for the sub-task "{title}".
Write the information down and make a proposal of how to solve the sub-task.
Do not explain your response or anything else. Just respond the relevant information for the sub-task and a potential solution.
""")
        body = body.replace(AGENT_NAME, AGENT_NAME[:3]+ "_" + AGENT_NAME[4:]) # prevent endless loops

        issue_number = Config.git_utilities.create_issue(repository, title, ai_remark + body)
        sub_issue_numbers.append(issue_number)

        if len(created_sub_tasks) == 0:
            created_sub_tasks = "## Other sub-tasks\nThe following sub-tasks have already been identified:\n"
        created_sub_tasks += f"### {title}\n{body}\n\n"

    # Create a comment on the main issue with the list of sub-issues
    sub_issue_links = "\n".join([f"- #{num}" for num in sub_issue_numbers])
    comment_text = f"Sub-issues have been created:\n{sub_issue_links}"
    Config.git_utilities.add_comment_to_issue(repository, issue, ai_remark + comment_text)

    return sub_issue_numbers