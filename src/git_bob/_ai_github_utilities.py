# This module contains utility functions for interacting with GitHub issues and pull requests using AI.
# It includes functions for setting up AI remarks, commenting on issues, reviewing pull requests, and solving issues.
import warnings

from ._logger import Log
import json
import os

SYSTEM_PROMPT = os.environ.get("SYSTEM_MESSAGE", "You are an AI-based coding assistant named git-bob. You are an excellent Python programmer and software engineer.")


def setup_ai_remark():
    """
    Set up the AI remark for comments.

    Returns
    -------
    str
        The AI remark string.
    """
    from git_bob import __version__
    from ._utilities import get_llm_name
    model = get_llm_name()
    return f"<sup>This message was generated by [git-bob](https://github.com/haesleinhuepf/git-bob) (version: {__version__}, model: {model}), an experimental AI-based assistant. It can make mistakes and has [limitations](https://github.com/haesleinhuepf/git-bob?tab=readme-ov-file#limitations). Check its messages carefully.</sup>"


def comment_on_issue(repository, issue, prompt_function):
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
    Log().log(f"-> comment_on_issue({repository}, {issue})")
    from ._github_utilities import get_conversation_on_issue, add_comment_to_issue, list_repository_files, \
        get_repository_file_contents
    from ._utilities import text_to_json, modify_discussion

    ai_remark = setup_ai_remark()

    discussion = modify_discussion(get_conversation_on_issue(repository, issue))
    print("Discussion:", discussion)

    all_files = "* " + "\n* ".join(list_repository_files(repository))

    relevant_files = prompt_function(f"""
{SYSTEM_PROMPT}
Decide what to do to respond to a github issue. The entire issue discussion is given and a list of all files in the repository.

## Discussion of the issue #{issue}

{discussion}

## All files in the repository

{all_files}

## Your task
Which of these files are necessary to read for solving the issue #{issue} ? Keep the list short.
Returning an empty list is also a valid answer.
Respond with the filenames as JSON list.
""")
    filenames = text_to_json(relevant_files)

    file_content_dict = get_repository_file_contents(repository, filenames)

    temp = []
    for k, v in file_content_dict.items():
        temp = temp + [f"### File {k} content\n\n```\n{v}\n```\n"]
    relevant_files_contents = "\n".join(temp)

    comment = prompt_function(f"""
{SYSTEM_PROMPT}
Respond to a github issue. Its entire discussion is given and additionally, content of some relevant files.

## Discussion

{discussion}

## Relevant files

{relevant_files_contents}

## Your task

Respond to the discussion above.
In case code-changes are discussed, make a proposal of how new code could look like.
Do NOT explain your response or anything else. 
Just respond to the discussion.
""")

    print("comment:", comment)

    add_comment_to_issue(repository, issue, f"""        
{ai_remark}

{comment}
""")


def review_pull_request(repository, issue, prompt_function):
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
    Log().log(f"-> review_pull_request({repository}, {issue})")
    from ._github_utilities import get_conversation_on_issue, add_comment_to_issue, get_diff_of_pull_request
    from ._utilities import modify_discussion

    ai_remark = setup_ai_remark()

    discussion = modify_discussion(get_conversation_on_issue(repository, issue))
    print("Discussion:", discussion)

    file_changes = get_diff_of_pull_request(repository, issue)

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

Review this pull-request and contribute to the discussion. 

Do NOT explain your response or anything else. 
Just respond to the discussion.
""")

    print("comment:", comment)

    add_comment_to_issue(repository, issue, f"""        
{ai_remark}

{comment}
""")


def summarize_github_issue(repository, issue, prompt_function):
    """
    Summarize a GitHub issue.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository.
    issue : int
        The issue number to summarize.
    llm_model : str
        The language model to use for generating the summary.
    """
    Log().log(f"-> summarize_github_issue({repository}, {issue})")
    from ._github_utilities import get_github_issue_details

    issue_conversation = get_github_issue_details(repository, issue)

    summary = prompt_function(f"""
Summarize the most important details of this issue #{issue} in the repository {repository}. 
In case filenames, variables and code-snippetes are mentioned, keep them in the summary, they are very important.

## Issue to summarize:
{issue_conversation}
""")

    print("Issue summary:", summary)
    return summary


def create_or_modify_file(repository, issue, filename, branch_name, issue_summary, prompt_function):
    """
    Create or modify a file in a GitHub repository.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository.
    issue : int
        The issue number to solve.
    filename : str
        The name of the file to create or modify.
    branch_name : str
        The name of the branch to create or modify the file in.
    issue_summary : str
        The summary of the issue to solve.
    prompt_function : function
        The function to generate the file modification content.
    """
    Log().log(f"-> create_or_modify_file({repository}, {issue}, {filename}, {branch_name})")
    from ._github_utilities import get_repository_file_contents, write_file_in_new_branch, create_branch, \
        check_if_file_exists, get_file_in_repository, execute_notebook_in_repository
    from ._utilities import remove_outer_markdown, split_content_and_summary, erase_outputs_of_code_cells, \
        restore_outputs_of_code_cells

    original_ipynb_file_content = None

    if check_if_file_exists(repository, branch_name, filename):
        file_content = get_file_in_repository(repository, branch_name, filename).decoded_content.decode()
        print(filename, "will be overwritten")
        if filename.endswith('.ipynb'):
            print("Removing outputs from ipynb file")
            original_ipynb_file_content = file_content
            file_content = erase_outputs_of_code_cells(file_content)
        file_content_instruction = f"""
Modify the file "{filename}" to solve the issue #{issue}.
Keep your modifications absolutely minimal.

That's the file "{filename}" content you will find in the file:
```
{file_content}
```

## Your task
Modify content of the file "{filename}" to solve the issue above.
Keep your modifications absolutely minimal.
Return the entire new file content, do not shorten it.
"""
    else:
        print(filename, "will be created")
        format_specific_instructions = ""
        if filename.endswith('.py'):
            format_specific_instructions = " When writing new functions, use numpy-style docstrings."
        elif filename.endswith('.ipynb'):
            format_specific_instructions = " In the new notebook file, write short code snippets in code cells and avoid long code blocks. Make sure everything is done step-by-step and we can inspect intermediate results. Add explanatory markdown cells in front of every code cell."
        file_content_instruction = f"""
Create the file "{filename}" to solve the issue #{issue}.{format_specific_instructions}

## Your task
Generate content for the file "{filename}" to solve the issue above.
Keep it short.
"""

    prompt = f"""
{SYSTEM_PROMPT}
Given a github issue summary (#{issue}) and optionally file content (filename {filename}), modify the file content or create the file content to solve the issue.

## Issue {issue} Summary

{issue_summary}

## File {filename} content

{file_content_instruction}


Respond ONLY the content of the file and afterwards a single line summarizing the changes you made (without mentioning the issue).
"""
    response = prompt_function(prompt)

    new_content, commit_message = split_content_and_summary(response)

    do_execute_notebok = False

    if original_ipynb_file_content is not None:
        try:
            new_content = restore_outputs_of_code_cells(new_content, original_ipynb_file_content)
        except ValueError as e:
            warnings.warn(f"Could not restore outputs of code cells in {filename}: {e}")
            do_execute_notebok = True

    elif filename.endswith('.ipynb'):
        print("Erasing outputs in generated ipynb file")
        new_content = erase_outputs_of_code_cells(new_content)
        do_execute_notebok = True

    print("New file content", new_content)
    print("Summary", commit_message)

    write_file_in_new_branch(repository, branch_name, filename, new_content + "\n", commit_message)

    if do_execute_notebok:
        print("Executing the notebook")
        execute_notebook_in_repository(repository, branch_name, filename)

    return commit_message


def solve_github_issue(repository, issue, llm_model, prompt_function, base_branch=None):
    """
    Attempt to solve a GitHub issue by modifying a single file and sending a pull-request.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository.
    issue : int
        The issue number to solve.
    llm_model : str
        The language model to use for generating the solution.
    prompt_function: function
        The function to use for generating prompts.
    base_branch : str
        The name of the base branch to create the new branch from.
    """
    # modified from: https://github.com/ScaDS/generative-ai-notebooks/blob/main/docs/64_github_interaction/solving_github_issues.ipynb

    Log().log(f"-> solve_github_issue({repository}, {issue})")

    from ._github_utilities import get_github_issue_details, list_repository_files, get_repository_file_contents, \
        write_file_in_new_branch, send_pull_request, add_comment_to_issue, create_branch, check_if_file_exists, \
        get_diff_of_branches, get_conversation_on_issue, rename_file_in_repository, delete_file_from_repository, \
        copy_file_in_repository, execute_notebook_in_repository, download_to_repository, add_comment_to_issue
    from ._utilities import remove_outer_markdown, split_content_and_summary, text_to_json, modify_discussion
    from github.GithubException import GithubException

    discussion = modify_discussion(get_conversation_on_issue(repository, issue))
    print("Discussion:", discussion)

    all_files = "* " + "\n* ".join(list_repository_files(repository))

    modifications = prompt_function(f"""
Given a list of files in the repository {repository} and a github issues description (# {issue}), determine which files need to be modified, renamed or deleted to solve the issue.

## Github Issue #{issue} Discussion

{discussion}

## All files in the repository

{all_files}

## Your task
Decide which of these files need to be modified, created, downloaded, renamed, copied, executed or deleted to solve #{issue} ? Downloads are necessary, if there is a url in the discussion and the linked file is needed in the proposed code.
Keep the list of actions minimarl.
Response format:
- For modifications: {{'action': 'modify', 'filename': '...'}}
- For creations: {{'action': 'create', 'filename': '...'}}
- For downloads: {{'action': 'download', 'source_url': '...', 'target_filename': '...'}}
- For renames: {{'action': 'rename', 'old_filename': '...', 'new_filename': '...'}}
- For copies: {{'action': 'copy', 'old_filename': '...', 'new_filename': '...'}}
- For executions: {{'action': 'execute', 'filename': '...'}}
- For deletions: {{'action': 'delete', 'filename': '...'}}
Respond with the actions as JSON list.
""")

    instructions = text_to_json(modifications)

    # create a new branch
    branch_name = create_branch(repository, parent_branch=base_branch)

    print("Created branch", branch_name)

    errors = []
    commit_messages = []
    for instruction in instructions:
        action = instruction.get('action')

        for filename_key in ["filename", "new_filename", "old_filename", "target_filename"]:
            if filename_key in instruction.keys():
                filename = instruction[filename_key]
                if filename.startswith(".github/workflows"):
                    errors.append(f"Error processing {filename}: Modifying workflow files is not allowed.")
                    continue

        try:
            if action == 'create':
                if check_if_file_exists(repository, branch_name, filename):
                    errors.append(f"Error processing {filename}: File already exists.")
                else:
                    message = filename + ":" + create_or_modify_file(repository, issue, filename, branch_name, discussion,
                                                                     prompt_function)
                    commit_messages.append(message)
            elif action == 'modify':
                filename = instruction['filename']
                message = filename + ":" + create_or_modify_file(repository, issue, filename, branch_name, discussion,
                                                                 prompt_function)
                commit_messages.append(message)
            elif action == 'download':
                source_url = instruction['source_url']
                target_filename = instruction['target_filename']
                download_to_repository(repository, branch_name, source_url, target_filename)
                commit_messages.append(f"Downloaded {source_url}, saved as {target_filename}.")
            elif action == 'rename':
                old_filename = instruction['old_filename']
                new_filename = instruction['new_filename']
                rename_file_in_repository(repository, branch_name, old_filename, new_filename)
                commit_messages.append(f"Renamed {old_filename} to {new_filename}.")
            elif action == 'delete':
                filename = instruction['filename']
                delete_file_from_repository(repository, branch_name, filename)
                commit_messages.append(f"Deleted {filename}.")
            elif action == 'copy':
                old_filename = instruction['old_filename']
                new_filename = instruction['new_filename']
                copy_file_in_repository(repository, branch_name, old_filename, new_filename)
                commit_messages.append(f"Copied {old_filename} to {new_filename}.")
            elif action == 'execute':
                filename = instruction['filename']
                print("Executing", filename)
                execute_notebook_in_repository(repository, branch_name, filename)
                commit_messages.append(f"Executed {filename}.")
        except Exception as e:
            errors.append(f"Error during {instruction}: " + str(e))

    error_messages = ""
    if len(errors) > 0:
        error_messages = "\n\nDuring solving this task, the following errors occurred:\n\n* " + "\n* ".join(
            errors) + "\n"

    print(error_messages)

    # get a diff of all changes
    diffs_prompt = get_diff_of_branches(repository, branch_name, base_branch=base_branch)

    # summarize the changes
    commit_messages_prompt = "* " + "\n* ".join(commit_messages)
    pull_request_summary = prompt_function(f"""
{SYSTEM_PROMPT}
Given a list of commit messages and a git diff, summarize the changes you made in the files.
You modified the repository {repository} to solve the issue #{issue}, which is also summarized below.

## Github Issue #{issue} Discussion

{discussion}

## Commit messages
You committed these changes to these files

{commit_messages_prompt}

## Git diffs
The following changes were made in the files:

{diffs_prompt}

## Your task
Summarize the changes above to a one paragraph line Github pull-request message. 
Afterwards, summarize the summary in a single line, which will become the title of the pull-request.
Do not add headline or any other formatting. Just respond with the paragraphe and the title in a new line below.
""")

    pull_request_description, pull_request_title = split_content_and_summary(pull_request_summary)

    try:
        send_pull_request(repository,
                      source_branch=branch_name,
                      target_branch=base_branch,
                      title=pull_request_title,
                      description=f"{pull_request_description} {error_messages}\n\ncloses #{issue}")
    except GithubException as e:
        add_comment_to_issue(repository, issue, f"Error creating pull-request: {e}{error_messages}")


def split_issue_in_sub_issues(repository, issue, prompt_function):
    """
    Split a main issue into sub-issues for each sub-task.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    issue : int
        The main issue number.
    """
    Log().log(f"-> split_issue_in_sub_issues({repository}, {issue},...)")
    from ._utilities import text_to_json
    from ._github_utilities import create_issue, add_comment_to_issue, get_conversation_on_issue

    discussion = get_conversation_on_issue(repository, issue)
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
        body = body.replace("git-bob", "git=bob") # prevent endless loops

        issue_number = create_issue(repository, title, ai_remark + body)
        sub_issue_numbers.append(issue_number)

        if len(created_sub_tasks) == 0:
            created_sub_tasks = "## Other sub-tasks\nThe following sub-tasks have already been identified:\n"
        created_sub_tasks += f"### {title}\n{body}\n\n"

    # Create a comment on the main issue with the list of sub-issues
    sub_issue_links = "\n".join([f"- #{num}" for num in sub_issue_numbers])
    comment_text = f"Sub-issues have been created:\n{sub_issue_links}"
    add_comment_to_issue(repository, issue, ai_remark + comment_text)

    return sub_issue_numbers


