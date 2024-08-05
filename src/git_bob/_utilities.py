# This module provides utility functions for text processing, including functions to remove indentation and outer markdown from text.
import sys
from functools import lru_cache
from functools import wraps
from toolz import curry

def remove_indentation(text):
    """
    Remove 4 spaces indentation from each line in the given text.

    Parameters
    ----------
    text : str
        The text from which to remove indentation.

    Returns
    -------
    str
        The text without 4 spaces indentation.
    """
    text = text.replace("\n    ", "\n")
    return text.strip()

def remove_outer_markdown(text):
    """
    Remove outer markdown syntax from the given text.

    Parameters
    ----------
    text : str
        The text from which to remove markdown.

    Returns
    -------
    str
        The text without outer markdown syntax.
    """
    text = text.strip("\n")

    possible_beginnings = ["```python", "```Python", "```nextflow", "```java", "```javascript", "```macro", "```groovy", "```jython", "```md", "```markdown",
                   "```txt", "```csv", "```yml", "```yaml", "```json", "```JSON", "```py", "<FILE>", "```"]

    possible_endings = ["```", "</FILE>"]

    for beginning in possible_beginnings:
        if text.startswith(beginning):
            text = text[len(beginning):]
            break

    for ending in possible_endings:
        if text.endsWith(ending):
            text = text[:-len(ending)]
            break

    text = text.strip("\n")

    return text

@lru_cache(maxsize=1)
def get_llm_name():
    """
    Get the name of the LLM (Large Language Model) to use.

    Returns
    -------
    str
        The name of the LLM.
    """
    import os
    return os.environ.get("GIT_BOB_LLM_NAME", "gpt-4o-2024-05-13")

class ErrorReporting:
    status = True

def report_error(message):
    """
    Report an error by logging it and adding a comment to a GitHub issue.

    Parameters
    ----------
    message : str
        The error message to report.
    """
    import sys
    import os
    from ._ai_github_utilities import setup_ai_remark
    from ._github_utilities import add_comment_to_issue
    from ._logger import Log

    if not ErrorReporting.status:
        return

    log = "\n".join(Log().get())

    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None
    run_id = os.environ.get("GITHUB_RUN_ID")
    ai_remark = setup_ai_remark()

    complete_error_message = remove_indentation(f"""
    {ai_remark}

    I'm sorry, I encountered an error while processing your request. Here is the error message:

    {message}

    This is how far I came:
    ```
    {log}
    ```

    [More Details...](https://github.com/{repository}/actions/runs/{run_id})
    """)
    add_comment_to_issue(repository, issue, complete_error_message)

@curry
def catch_error(func):
    """
    Decorator to catch and report errors in a function.

    Parameters
    ----------
    func : callable
        The function to wrap.

    Returns
    -------
    callable
        The wrapped function.
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

def split_content_and_summary(text):
    """
    Split a text into content and summary, assuming the summary is the last line.

    Parameters
    ----------
    text : str
        The text to split.

    Returns
    -------
    tuple
        A tuple containing the content and the summary.
    """
    temp = text.split("\n")
    summary = temp[-1]
    remaining_content = temp[:-1]
    if len(summary) < 5:
        summary = temp[-2]
        remaining_content = temp[:-2]

    new_content = remove_outer_markdown("\n".join(remaining_content))

    return new_content, summary

def split_after_token(text, token):
    """
    Split the text after the first occurrence of a specified token.

    Parameters
    ----------
    text : str
        The text to split.
    token : str
        The token to split after.

    Returns
    -------
    str
        The text after the token.
    """
    if token not in text:
        return text
    return text.split(token)[1]