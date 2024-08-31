# This module provides utility functions for text processing, including functions to remove indentation and outer markdown from text.
import sys
from functools import lru_cache
from functools import wraps
from toolz import curry


def remove_outer_markdown(text):
    """
    Remove outer markdown syntax from the given text.

    Parameters
    ----------
    text : str
        The input text with potential markdown syntax.

    Returns
    -------
    str
        The text with outer markdown syntax removed and stripped.
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
        if text.endswith(ending):
            text = text[:-len(ending)]
            break

    text = text.strip("\n")

    return text

@lru_cache(maxsize=1)
def get_llm_name():
    """
    Get the name of the LLM from environment variables.

    Returns
    -------
    str
        The name of the LLM.
    """
    import os
    return os.environ.get("GIT_BOB_LLM_NAME", "gpt-4o-2024-08-06")


class ErrorReporting:
    status = False


def quick_first_response():
    """
    Response to a comment to the GitHub issue just mentioning that we're on it.

    Parameters
    ----------
    message : str
        The error message to be reported.
    """
    import sys
    import os
    from ._ai_github_utilities import setup_ai_remark
    from ._github_utilities import add_comment_to_issue, add_reaction_to_last_comment_in_issue

    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None
    run_id = os.environ.get("GITHUB_RUN_ID")
    ai_remark = setup_ai_remark()

    # add reaction to issue
    add_reaction_to_last_comment_in_issue(repository, issue, "+1")


def split_content_and_summary(text):
    """
    Split the given text into content and summary.

    Assuming a text consists of a task solution (code, text) and a summary in the last line,
    it splits the text into the content and the summary.

    Parameters
    ----------
    text : str
        The input text containing content and summary.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - str: The content with outer markdown removed.
        - str: The summary.
    """
    text = text.strip("\n").strip()
    temp = text.split("\n")
    summary = temp[-1].strip()
    remaining_content = temp[:-1]
    if len(summary) < 5:
        summary = temp[-2]
        remaining_content = temp[:-2]

    new_content = remove_outer_markdown("\n".join(remaining_content))

    return new_content.strip(), summary.strip()


def erase_outputs_of_code_cells(file_content):
    """
    Erase outputs of code cells in a Jupyter notebook.

    Parameters
    ----------
    notebook : str
        The notebook content as a string.
    """
    import json
    notebook = json.loads(file_content)
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
    file_content = json.dumps(notebook, indent=1)
    return file_content


def text_to_json(text):
    """Converts a string, e.g. a response from an LLM, to a valid JSON object."""
    import json
    if "[" in text:
        text = "[" +  text.split("[")[1]
    if "]" in text:
        text = text.split("]")[0] + "]"

    print("JSON?:", text)

    return json.loads(text)


def modify_discussion(discussion):
    import re
    from ._github_utilities import get_conversation_on_issue, get_diff_of_pull_request, get_repository_file_contents

    # Regex to find URLs in the discussion
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, discussion)

    # Function to check if URL is a GitHub issue, pull request or file path
    def is_github_url(url):
        if 'github.com' not in url:
            return None
        if '/issues/' in url:
            return 'issue'
        elif '/pull/' in url:
            return 'pull_request'
        elif 'blob/' in url:
            return 'file'
        return None

    # Placeholder for additional content extracted from URLs
    additional_content = ""

    # Process each URL based on its type
    for url in urls:
        url_type = is_github_url(url)
        if url_type == 'issue':
            parts = url.split('/')
            repo = parts[3] + '/' + parts[4]
            issue_number = int(parts[-1])
            additional_content += get_conversation_on_issue(repo, issue_number)
        elif url_type == 'pull_request':
            parts = url.split('/')
            repo = parts[3] + '/' + parts[4]
            pr_number = int(parts[-1])
            # Get both the diff and discussion on pull request
            additional_content += get_conversation_on_issue(repo, pr_number)
            additional_content += get_diff_of_pull_request(repo, pr_number)
        elif url_type == 'file':
            parts = url.split('/')
            repo = parts[3] + '/' + parts[4]
            branch_name = parts[-3]
            file_path = '/'.join(parts[7:])
            file_contents = get_repository_file_contents(repo, [file_path])
            additional_content += file_contents.get(file_path, '')

    # Modify the existing discussion content
    discussion = discussion.replace("\n#", "\n###")
    discussion = re.sub(r'<sup>.*?</sup>', '', discussion)

    # Append the additional content to the discussion before returning
    return discussion + "\n\n" + additional_content
