@catch_error
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
    """
    Log().log(f"-> create_or_modify_file({repository}, {issue}, {filename}, {branch_name})")
    from ._github_utilities import get_repository_file_contents, write_file_in_new_branch, create_branch, check_if_file_exists, get_file_in_repository
    from ._utilities import remove_outer_markdown, split_content_and_summary

    if check_if_file_exists(repository, branch_name, filename):
        file_content = get_file_in_repository(repository, branch_name, filename).decoded_content.decode()
        print(filename, "will be overwritten")
        if filename.endswith('.ipynb'):
            notebook = json.loads(file_content)
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    cell['outputs'] = []
                    cell['execution_count'] = None
            file_content = json.dumps(notebook, indent=1)
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
"""
    else:
        print(filename, "will be created")
        file_content_instruction = f"""
Create the file "{filename}" to solve the issue #{issue}.

## Your task
Generate content for the file "{filename}" to solve the issue above.
Keep it short.
"""

    response = prompt_function(f"""
{SYSTEM_PROMPT}
Given a github issue summary (#{issue}) and optionally file content (filename {filename}), modify the file content or create the file content to solve the issue.

## Issue {issue} Summary

{issue_summary}

## File {filename} content

{file_content_instruction}


Respond ONLY the content of the file and afterwards a single line summarizing the changes you made (without mentioning the issue).
""")

    new_content, commit_message = split_content_and_summary(response)


    print("New file content", new_content)
    print("Summary", commit_message)

    write_file_in_new_branch(repository, branch_name, filename, new_content + "\n", commit_message)

    return commit_message
