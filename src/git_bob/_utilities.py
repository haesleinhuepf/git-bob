# This module provides utility functions for text processing, including functions to remove indentation and outer markdown from text.
import sys
from functools import lru_cache
from functools import wraps
from toolz import curry

def remove_indentation(text):
    """
    Remove indentation from the given text.

    Parameters
    ----------
    text : str
        The text from which to remove indentation.

    Returns
    -------
    str
        The text without indentation.
    """
    text = text.replace("\n    ", "\n")

    return text.strip()

def remove_outer_markdown(text):
    """
    Remove outer markdown from the given text.

    Parameters
    ----------
    text : str
        The text from which to remove outer markdown.

    Returns
    -------
    str or None
        The text without outer markdown, or None if no markdown was found.
    """
    code = text \
        .replace("```python", "```") \
        .replace("```Python", "```") \
        .replace("```nextflow", "```") \
        .replace("```java", "```") \
        .replace("```javascript", "```") \
        .replace("```macro", "```") \
        .replace("```groovy", "```") \
        .replace("```jython", "```") \
        .replace("```md", "```") \
        .replace("```markdown", "```") \
        .replace("```txt", "```") \
        .replace("```csv", "```") \
        .replace("```yml", "```") \
        .replace("```yaml", "```") \
        .replace("```json", "```") \
        .replace("```py", "```")

    parts = code.split("```")
    if len(parts) == 1:
        code = None
    else:
        code = ""
        for t, c in zip(parts[::2], parts[1::2]):
            code = code + c
        code = code.strip("\n")

    return code

@lru_cache(maxsize=1)
def get_llm_name():
    """
    Get the name of the language model (LLM) from the environment variable.

    Returns
    -------
    str
        The name of the LLM.
    """
    import os
    return os.environ.get("GIT_BOB_LLM_NAME", "gpt-4o-2024-05-13")

def report_error(message):
    """
    Report an error by adding a comment to the GitHub issue.

    Parameters
    ----------
    message : str
        The error message to report.
    """
    import sys
    import os
    from ._ai_github_utilities import setup_ai_remark
    from ._github_utilities import add_comment_to_issue

    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None
    run_id = os.environ.get("GITHUB_RUN_ID")
    ai_remark = setup_ai_remark()

    complete_error_message = remove_indentation(f"""
    {ai_remark}
    
    I'm sorry, I encountered an error while processing your request. Here is the error message:
    
    {message}
    
    [More Details...](https://github.com/{repository}/actions/runs/{run_id})
    """)
    add_comment_to_issue(repository, issue, complete_error_message)

@curry
def catch_error(func):
    """
    Decorator to catch and report errors in the decorated function.

    Parameters
    ----------
    func : function
        The function to decorate.

    Returns
    -------
    function
        The decorated function with error catching.
    """
    @wraps(func)
    def worker_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            name = func.__name__
            print(f"Error in {name}: {str(e)}")
            report_error(f"Error in {name}: {str(e)}")
            raise e

    return worker_function
