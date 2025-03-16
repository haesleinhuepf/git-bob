
POSSBILE_MARKDOWN_FENCES = ["```python", "```Python", "```nextflow", "```java", "```javascript", "```macro", "```groovy",
                           "```jython", "```md", "```markdown", "```plaintext", "```tex", "```latex",
                           "```txt", "```csv", "```yml", "```yaml", "```json", "```JSON", "```py", "```svg", "```xml", "<FILE>", "```"]

def clean_output(repository, text):
    #from ._github_utilities import get_contributors
    # if all lines start with spaces (except 1st and last), remove those spaces in all lines
    from ._config import Config
    lines = text.split("\n")
    while (True):
        if all([line.startswith(" ") for line in lines[1:]]):
            text = lines[0] + "\n" + "\n".join([line[1:] for line in lines[1:]])
            lines = text.split("\n")
        else:
            break

    # if text starts with ```markdown, remove that
    while text.startswith("\n") or text.startswith(" "):
        text = text.strip("\n").strip(" ")
    text = remove_outer_markdown(text)

    # if there are strangers tagged, remove those tags
    temp = text.split("```")
    for i in range(0, len(temp), 2):
        temp[i] = temp[i].replace("@", "@ ")
    text = "```".join(temp)
    contributors = Config.git_utilities.get_contributors(repository)
    for c in contributors:
        text = text.replace("@ " + c, "@" + c)
    return text


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
    text = text.strip("\n").strip(" ")

    possible_beginnings = POSSBILE_MARKDOWN_FENCES

    possible_endings = ["```", "</FILE>"]

    if any([text.startswith(beginning) for beginning in possible_beginnings]) and any([text.endswith(ending) for ending in possible_endings]):

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


def modify_discussion(discussion, prompt_visionlm=None):
    import re
    import os
    import docx2markdown
    from ._config import Config, VISION_SYSTEM_MESSAGE, TEXT_FILE_ENDINGS
    from ._git import is_github_url
    from ._io import download_url, load_image_from_url, read_text_file
    from ._ipynb import erase_outputs_of_code_cells

    # from ._github_utilities import get_conversation_on_issue, get_diff_of_pull_request, get_file_in_repository

    if prompt_visionlm is None:
        from .._endpoints import prompt_openai
        prompt_visionlm = prompt_openai

    # Regex to find URLs in the discussion
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, discussion)

    # Placeholder for additional content extracted from URLs
    additional_content = {}

    # Process each URL based on its type
    for url in urls:
        if url.endswith(")"):  # happens with ![](url) syntax
            url = url[:-1]
        if url.endswith("'"):
            url = url[:-1]
        if url.endswith('"'):
            url = url[:-1]

        url_type = is_github_url(url)
        print("URL:", url)
        print("Type:", url_type)
        from datetime import datetime

        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if "### File {url} content" in discussion:
            continue

        try:
            if url_type == 'issue':
                parts = url.split('/')
                repo = parts[3] + '/' + parts[4]
                try:
                    issue_number = int(parts[-1])
                except:
                    continue
                additional_content[url] = Config.git_utilities.get_conversation_on_issue(repo, issue_number)
            elif url_type == 'pull_request':
                parts = url.split('/')
                repo = parts[3] + '/' + parts[4]
                try:
                    pr_number = int(parts[-1])
                except:
                    continue

                # Get both the diff and discussion on pull request
                additional_content[url] = (Config.git_utilities.get_conversation_on_issue(repo, pr_number) +
                                           Config.git_utilities.get_diff_of_pull_request(repo, pr_number))
            elif url_type == 'file':
                parts = url.split('/')
                # repo = parts[3] + '/' + parts[4]
                # branch_name = parts[6]
                file_path = '/'.join(parts[7:])
                temp_file_name = current_datetime + "_" + file_path.split('/')[-1]
                url = url.replace("/blob/", "/raw/")
                download_url(url, temp_file_name)
                # file_contents = Config.git_utilities.get_file_in_repository (repo, branch_name, file_path).decoded_content.decode()
                if url.endswith('.ipynb'):
                    file_contents = read_text_file(temp_file_name)
                    file_contents = erase_outputs_of_code_cells(file_contents)
                elif url.endswith('.docx'):
                    docx2markdown.docx_to_markdown(temp_file_name, temp_file_name + ".md")
                    file_contents = read_text_file(temp_file_name + ".md")
                    # remove the file
                    os.remove(temp_file_name + ".md")
                else:
                    file_contents = read_text_file(temp_file_name)

                os.remove(temp_file_name)

                additional_content[url] = file_contents
            elif url_type == 'image':
                image = load_image_from_url(url)
                image_content = prompt_visionlm(VISION_SYSTEM_MESSAGE + "\n\nDescribe this image.", image=image)
                additional_content[url] = image_content
        except Exception as e:
            print(f"Error while processing URL {url}: {e}")

    # read local files
    temp = discussion.replace("\n", " ")
    for potential_filename in temp.split(" "):
        if len(potential_filename) < 4:  # too short to be a filename
            continue
        # check if file exists
        if os.path.exists(potential_filename):
            if potential_filename.endswith('.ipynb'):
                file_contents = read_text_file(potential_filename)
                file_contents = erase_outputs_of_code_cells(file_contents)
            elif potential_filename.endswith('.docx'):
                docx2markdown.docx_to_markdown(potential_filename, potential_filename + ".md")
                file_contents = read_text_file(potential_filename + ".md")
                # remove the file
                os.remove(potential_filename + ".md")
            elif any([potential_filename.endswith(f) for f in TEXT_FILE_ENDINGS]):
                file_contents = read_text_file(potential_filename)
            else:
                continue

            additional_content[potential_filename] = file_contents

    # Modify the existing discussion content
    discussion = discussion.replace("\n#", "\n###")
    discussion = re.sub(r'<sup>.*?</sup>', '', discussion)

    # Append the additional content to the discussion before returning
    temp = []
    for k, v in additional_content.items():
        temp = temp + [f"### File {k} content\n\n```\n{v}\n```\n"]

    return discussion + "\n\n" + "\n".join(temp)


def append_result(a, b):
    """
    Appends two strings, which might be produced by LLMs. E.g. in case the first thing contains ```python and the second
    starts with ```python, the beginning of the second string is removed.
    """
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a

    possible_beginnings = POSSBILE_MARKDOWN_FENCES

    for beginning in possible_beginnings:
        if beginning in a and b.startswith(beginning + "\n"):
            b = b[len(beginning):]
            return a + b
    return a + b


def remove_ansi_escape_sequences(text):
    import re
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def redact_text(text):
    """Hide sensitive information from a string"""
    import os
    from ._env import SENSIBLE_ENV_KEYS
    for key in SENSIBLE_ENV_KEYS:
        if key in os.environ and len(os.environ.get(key)) > 0:
            text = text.replace(os.environ.get(key), "***")
    return text


def file_list_from_commit_message_dict(repository, branch_name, commit_messages):
    """Takes commit messages and produces markdown-style links for a commit message where users can click to see files"""
    from ._config import Config, IMAGE_FILE_ENDINGS
    list_of_links = []
    for k, v in commit_messages.items():

        if "https://github.com/" in Config.git_server_url:
            url_template = f"{Config.git_server_url}{repository}/blob/{branch_name}/"
        else:
            url_template = f"{Config.git_server_url}{repository}/-/blob/{branch_name}/"

        suffix = ""
        prefix = ""
        if any([k.endswith(f) for f in IMAGE_FILE_ENDINGS]):
            prefix = "!"
            if "https://github.com/" in Config.git_server_url:
                suffix = "?raw=true"
            else:
                url_template = url_template.replace("/blob/", "/raw/")

        list_of_links.append(f"{prefix}[{k}]({url_template}{k}{suffix})")
    return list_of_links


def ensure_images_shown(markdown, list_of_markdown_image_links):
    """
    If [bla](bla.png) in markdown, but not ![bla](bla.png), add the ! in front.
    """

    for i in list_of_markdown_image_links:
        if i[0] == "!":
            if i[1:] in markdown and i not in markdown:
                markdown = markdown.replace(i[1:], i)
    return markdown


def setup_ai_remark():
    """
    Set up the AI remark for comments.

    Returns
    -------
    str
        The AI remark string.
    """
    from git_bob import __version__
    from ._config import Config, AGENT_NAME
    model = Config.llm_name
    run_id = Config.run_id
    repository = Config.repository
    if run_id is not None and Config.running_in_github_ci:
        link = f""", [log](https://github.com/{repository}/actions/runs/{run_id})"""
    else:
        link = ""
    if AGENT_NAME != "git-bob":
        agent_name = AGENT_NAME + " / [git-bob"
    else:
        agent_name = "[" + AGENT_NAME

    remarks = "".join(Config.remarks)
    return f"<sup>This message was generated by {agent_name}](https://github.com/haesleinhuepf/git-bob) (version: {__version__}, model: {model}{link}), an experimental AI-based assistant. It can make mistakes and has [limitations](https://github.com/haesleinhuepf/git-bob?tab=readme-ov-file#limitations). Check its messages carefully. {remarks}</sup>"


def text_to_json(text):
    """Converts a string, e.g. a response from an LLM, to a valid JSON object."""
    import json
    import re

    text = re.sub(r'[\x00-\x1f\x7f]', '', text)

    if "[" in text:
        text = "[" +  text.split("[")[1]
    if "]" in text:
        text = text.split("]")[0] + "]"
    text = text.replace("'", "\"")

    print("JSON?:", text)

    return json.loads(text)
