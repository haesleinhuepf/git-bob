def erase_outputs_of_code_cells(notebook):
    """
    Erase outputs of code cells in a Jupyter notebook.

    Parameters
    ----------
    notebook : dict
        The notebook content as a dictionary.
    """
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None

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
    from ._github_utilities import get_repository_file_contents, write_file_in_new_branch, create_branch, check_if_file_exists, get_file_in_repository
    from ._utilities import remove_outer_markdown, split_content_and_summary

    original_ipynb_file_content = None

    if check_if_file_exists(repository, branch_name, filename):
        file_content = get_file_in_repository(repository, branch_name, filename).decoded_content.decode()
        print(filename, "will be overwritten")
        if filename.endswith('.ipynb'):
            print("Removing outputs from ipynb file")
            original_ipynb_file_content = file_content
            notebook = json.loads(file_content)
            erase_outputs_of_code_cells(notebook)
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
        if filename.endswith('.ipynb'):
            notebook = {"cells": [], "metadata": {}}
            erase_outputs_of_code_cells(notebook)
            file_content = json.dumps(notebook, indent=1)
            file_content_instruction = f"""
Create the file "{filename}" as a notebook with erased outputs.

That's the file "{filename}" content:
```
{file_content}
```
"""
        else:
            file_content_instruction = f"""
Create the file "{filename}" to solve the issue #{issue}.

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

    if original_ipynb_file_content is not None:
        print("Recovering outputs in ipynb file")
        original_notebook = json.loads(original_ipynb_file_content)
        new_notebook = json.loads(new_content)

        original_code_cells = [cell for cell in original_notebook['cells'] if cell['cell_type'] == 'code']
        new_code_cells = [cell for cell in new_notebook['cells'] if cell['cell_type'] == 'code']

        for o_cell, n_cell in zip(original_code_cells, new_code_cells):
            if "\n".join(o_cell['source']).strip() == "\n".join(n_cell['source']).strip():
                print("Original cell content", o_cell)
                print("New cell content", n_cell)
                if "outputs" in o_cell.keys():
                    n_cell['outputs'] = o_cell['outputs']
                    n_cell['execution_count'] = o_cell['execution_count']
            else: # if code is different, any future results may be different, too
                print("codes no longer match")
                break

        new_content = json.dumps(new_notebook, indent=1)
    print("New file content", new_content)
    print("Summary", commit_message)

    write_file_in_new_branch(repository, branch_name, filename, new_content + "\n", commit_message)

    return commit_message
