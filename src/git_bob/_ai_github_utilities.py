def create_or_modify_file(repository, issue, filename, branch_name, issue_summary, prompt_function):
    """
    Create or modify a file in a GitHub repository.

    ...

    else:
        print(filename, "will be created")
        specific_instructions = ""
        if filename.endswith('.py'):
            specific_instructions = " Use numpy-style docstrings for functions."
        elif filename.endswith('.ipynb'):
            specific_instructions = " Include short code snippets in code cells, explanatory markdown cells before each code cell, and no long code blocks."
        
        file_content_instruction = f"""
Create the file "{filename}" to solve the issue #{issue}.{specific_instructions}

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
    ...
