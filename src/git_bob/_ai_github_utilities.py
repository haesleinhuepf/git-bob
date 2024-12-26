# This module contains utility functions for interacting with GitHub issues and pull requests using AI.
# It includes functions for setting up AI remarks, commenting on issues, reviewing pull requests, and solving issues.
import os
import warnings

from ._logger import Log

AGENT_NAME = os.environ.get("GIT_BOB_AGENT_NAME", "git-bob")
SYSTEM_PROMPT = os.environ.get("SYSTEM_MESSAGE", f"You are an AI-based coding assistant named {AGENT_NAME}. You are an excellent Python programmer and software engineer.")


def draw_vector_graphics(prompt: str, prompt_function: callable) -> str:
    """Generate SVG vector graphics based on a text prompt using an AI model.
    
    Parameters
    ----------
    prompt : str
        High-level description of what should be drawn
    prompt_function : callable
        Function that generates SVG content from a prompt
        
    Returns
    -------
    str
        Generated SVG file content
    """
    detailed_prompt = f"""Please create an SVG graphic that represents: {prompt}
    
    The response should:
    * Be a valid SVG file
    * Start with <?xml version="1.0" encoding="UTF-8"?>
    * Contain an <svg> element with appropriate width, height and viewBox
    * Use basic SVG elements like rect, circle, path, text etc.
    * Only contain the SVG code, no explanation
    """
    
    # Get the SVG content using the provided prompt function
    svg_content = prompt_function(detailed_prompt)
    
    return svg_content


def setup_ai_remark():
    """
    Set up the AI remark for comments.

    Returns
    -------
    str
        The AI remark string.
    """
    from git_bob import __version__
    from ._utilities import Config
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

    return f"<sup>This message was generated by {agent_name}](https://github.com/haesleinhuepf/git-bob) (version: {__version__}, model: {model}{link}), an experimental AI-based assistant. It can make mistakes and has [limitations](https://github.com/haesleinhuepf/git-bob?tab=readme-ov-file#limitations). Check its messages carefully.</sup>"


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
    from ._utilities import text_to_json, modify_discussion, clean_output, redact_text, Config

    ai_remark = setup_ai_remark()

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

    Config.git_utilities.add_comment_to_issue(repository, issue, f"""        
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
    from ._utilities import modify_discussion, clean_output, redact_text, Config

    ai_remark = setup_ai_remark()

    discussion = modify_discussion(Config.git_utilities.get_conversation_on_issue(repository, issue), prompt_visionlm=prompt_function)
    print("Discussion:", discussion)

    file_changes = Config.git_utilities.get_diff_of_pull_request(repository, issue)

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

Review this pull-request and contribute to the discussion as if you were a human talking to a human. 
Respond as if you were a human talking to a human.

Do NOT explain your response or anything else. 
Just respond to the discussion.
""")
    comment = redact_text(clean_output(repository, comment))

    print("comment:", comment)

    Config.git_utilities.add_comment_to_issue(repository, issue, f"""        
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
    from ._utilities import Config

    issue_conversation = Config.git_utilities.get_issue_details(repository, issue)

    summary = prompt_function(f"""
Summarize the most important details of this issue #{issue} in the repository {repository}. 
In case filenames, variables and code-snippetes are mentioned, keep them in the summary, they are very important.

## Issue to summarize:
{issue_conversation}
""")

    print("Issue summary:", summary)
    return summary


def fix_error_in_notebook(new_content, error_message, prompt_function):
    """
    Attempt to fix an error in a Jupyter notebook.

    Parameters
    ----------
    new_content : str
        The content of the notebook.
    error_message : str
        The error message.

    Returns
    -------
    str
        The fixed content of the notebook.
    str
        A summary of the changes made.
    """
    Log().log(f"-> fix_error_in_notebook(..., ...)")
    from ._utilities import erase_outputs_of_code_cells
    from ._utilities import split_content_and_summary

    notebook_without_output = erase_outputs_of_code_cells(new_content)

    prompt = f"""
    {SYSTEM_PROMPT}
    Given a Jupyter Notebook file content and an error message, modify the file content to solve the error. Return the notebook in JSON format!

    ## Jupyter Notebook file content 

    {new_content}
    
    ## Error message
    
    {error_message}

    Respond ONLY the content of the file and afterwards a single line summarizing the changes you made (without mentioning the issue).
    """
    print("Prompting for bug-fixed file content...")
    response = prompt_function(prompt)

    new_content, commit_message = split_content_and_summary(response)

    return new_content, commit_message


def create_or_modify_file(repository, issue, filename, branch_name, issue_summary, prompt_function, number_of_attempts:int=3):
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

    Returns
    -------
    dictionary of filename: commit_message for all created files
    """
    Log().log(f"-> create_or_modify_file({repository}, {issue}, {filename}, {branch_name})")
    from ._utilities import split_content_and_summary, erase_outputs_of_code_cells, restore_outputs_of_code_cells, execute_notebook, text_to_json, save_and_clear_environment, restore_environment, redact_text, Config, get_file_info, get_modified_files
    import os
    import docx2markdown
    from ._utilities import read_text_file, write_text_file, write_binary_file, read_binary_file
    from datetime import datetime

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    image_file_endings = [".png", ".jpg", ".jpeg", ".gif"]

    created_files = {}
    for attempt in range(number_of_attempts):
        an_error_happened = False

        created_files = {}
        original_ipynb_file_content = None

        format_specific_instructions = ""
        if any([filename.endswith(f) for f in image_file_endings]):
            print(f"Cannot create or modify image files like {filename}.")
            return created_files
        elif filename.endswith('.py'):
            format_specific_instructions = " When writing new functions, use numpy-style docstrings."
        elif filename.endswith('.ipynb'):
            format_specific_instructions = " In the notebook file, write short code snippets in code cells and avoid long code blocks. Make sure everything is done step-by-step and we can inspect intermediate results. Add explanatory markdown cells in front of every code cell. The notebook has NO cell outputs! Make sure that there is code that saves results such as plots, images or dataframes, e.g. as .png or .csv files. Numpy images have to be converted to np.uint8 before saving as .png. Plots must be saved to disk before the cell ends or it is shown. The notebook must be executable from top to bottom without errors. Return the notebook in JSON format!"
        elif filename.endswith('.docx'):
            format_specific_instructions = " Write the document in simple markdown format."
        elif filename.endswith('.pptx'):
            format_specific_instructions = """
The file should be a presentation with slides, formatted as a JSON list containing dictionaries with a 'title' and a 'content' list with up to 2 strings.
These strings can be text+text or text+image. The strings can be multi-line text, and also be file-paths of .jpg, .gif or .png files. 
If it's an image, it MUST only be the file-path and no additional text.
If it's text, make sure the text is short enough that it fits on a slide. Also put enough information on a slide so that it doesn't appear empty. Two to four sentences per slide are nice. For more detailed information consider using bullet-points instead of long sentences. Four to six bullet points per slide are great.
The first slide contains only the author name as single string in the list of contents.
Choose from these existing files and only use them if they fit well to the content:\n* """ + \
                "\n* ".join(Config.git_utilities.list_repository_files(repository, branch_name=branch_name, file_patterns=image_file_endings)) + "\n\n" + \
                """
Examples for slides:
Example 1: {"title":"Continents and backing", "content":["Author1 name, Author2 name, ..."]}
Example 2: {"title":"Continents", "content":["The planet is separated into continents", "Each continent consists of countries, which might be further structured into federal districts"]}
Example 3: {"title":"Backing cake", "content":["When baking cake it is important to pre-heat the oven before putting the cake in.", "Ingredients: \n  * Flour\n  * Sugar\n  * Salt\n  * Eggs"]}
Example 4: {"title":"Regional food", "content":["Depending on the continent, regional food cultures have developed over the centures.", "These traditions developed because of availability of different ingredients and also depending on other natural resources.", "For example, in antarctical, wine grows relatively badly. That's why there are no traditional wines from Antarctica and wine needs to be imported in case it is an ingredient for a certain food. Hence, no traditional food from Antarctical is made of wine."]}
Example 5: {"title":"Summary", "content":["In this slide-deck we learned about\n* Continents\n* Backing\n* Regional differences in food culture", "earth.png"]}
"""
        elif filename.endswith('.svg'):
            new_content = draw_vector_graphics(issue_summary, prompt_function)
            Config.git_utilities.write_file_in_branch(repository, branch_name, filename, new_content, "Added SVG file")
            return {filename: "Added SVG file"}

        file_content = None
        if Config.git_utilities.check_if_file_exists(repository, branch_name, filename):
            try:
                file_content = Config.git_utilities.decode_file(Config.git_utilities.get_file_in_repository(repository, branch_name, filename))
            except UnicodeDecodeError:
                pass # happens when attempting to modify binary files

        if file_content is not None:
            print(filename, "will be overwritten")
            if filename.endswith('.ipynb'):
                print("Removing outputs from ipynb file")
                original_ipynb_file_content = file_content
                file_content = erase_outputs_of_code_cells(file_content)
            elif filename.endswith('.docx'):
                docx2markdown.docx_to_markdown(filename, filename + current_datetime + ".md")
                file_content = read_text_file(filename + current_datetime + ".md")

            file_content_instruction = f"""
Modify the file "{filename}" to solve the issue #{issue}. {format_specific_instructions}
If the discussion is long, some stuff might be already done. In that case, focus on what was said at the very end in the discussion.
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
            file_content_instruction = f"""
Create the file "{filename}" to solve the issue #{issue}. {format_specific_instructions}

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
        print("Prompting for new file content...")
        response = prompt_function(prompt)

        new_content, commit_message = split_content_and_summary(response)

        print("New file content", len(new_content), "\n------------\n", new_content[:200], "\n------------")

        do_execute_notebook = False
        print("Summary", commit_message)

        if original_ipynb_file_content is not None:
            try:
                new_content = restore_outputs_of_code_cells(new_content, original_ipynb_file_content)
            except ValueError as e:
                warnings.warn(f"Could not restore outputs of code cells in {filename}: {e}")
                do_execute_notebook = True

        elif filename.endswith('.ipynb'):
            print("Erasing outputs in generated ipynb file")
            new_content = erase_outputs_of_code_cells(new_content)
            do_execute_notebook = True
        elif filename.endswith('.docx'):
            write_text_file(filename + current_datetime + ".md", new_content)
            docx2markdown.markdown_to_docx(filename + current_datetime + ".md", filename)
            # workaround to make sure the file can be read by word later
            docx2markdown.docx_to_markdown(filename, filename + current_datetime + ".md")
            docx2markdown.markdown_to_docx(filename + current_datetime + ".md", filename)
            new_content = read_binary_file(filename)
            # delete temporary markdown file
            os.remove(filename + current_datetime + ".md")
        elif filename.endswith('.pptx'):
            from ._utilities import make_slides
            make_slides(new_content, filename)
            new_content = read_binary_file(filename)

        if do_execute_notebook:
            print("Executing the notebook", len(new_content))
            current_dir = os.getcwd()
            print("current_dir", current_dir)
            path_without_filename = os.path.dirname(filename)
            print("path_without_filename", path_without_filename)
            if len(path_without_filename) > 0:
                os.makedirs(path_without_filename, exist_ok=True)
                os.chdir(path_without_filename)

            not_executed_notebook = new_content

            # read existing files + creation dates recursively
            file_info = get_file_info()

            # Execute the notebook
            try:
                for num_attempt in range(0, number_of_attempts):
                    saved_environment = save_and_clear_environment()
                    new_content, error_message = execute_notebook(new_content)
                    restore_environment(saved_environment)
                    if error_message is None:
                        break

                    if num_attempt == number_of_attempts - 1:
                        print("Error during final notebook execution", error_message)
                        break # do not remove files again if this was the last attempt

                    Config.git_utilities.write_file_in_branch(repository, branch_name, filename, new_content,
                                                             redact_text(commit_message) + "(containing error)")
                    print("Error during notebook execution, trying again because:", error_message)
                    list_of_files = get_modified_files(file_info)
                    print("------------------------")
                    for file in list_of_files:
                        print("Remove file created by notebook:", file, os.path.exists(file))
                        if os.path.exists(file):
                            os.remove(file)
                    print("------------------------")
                    new_content, commit_message = fix_error_in_notebook(new_content, error_message, prompt_function)


                # scan for files the notebook created
                list_of_files = get_modified_files(file_info)
                print("------------------------")
                for file in list_of_files:
                    print("File created by notebook:", file, os.path.exists(file))
                    if os.path.exists(file):
                        created_files[file] = f"Adding {path_without_filename}/{file} created by notebook"
                        with open(file, 'rb') as f:
                            file_content2 = f.read()
                            Config.git_utilities.write_file_in_branch(repository, branch_name, f"{file}", file_content2, created_files[file])
                print("------------------------")

            except Exception as e:
                raise ValueError(f"Error during notebook execution: {e}")
            finally:
                os.chdir(current_dir)
                restore_environment(saved_environment)

            print("Executed notebook", len(new_content))

        if isinstance(new_content, str):
            new_content = redact_text(new_content) + "\n"
        if not an_error_happened:
            break
        print(f"An error happened. Retrying... {attempt+1}/{number_of_attempts}")

    Config.git_utilities.write_file_in_branch(repository, branch_name, filename, new_content, redact_text(commit_message))
    created_files[filename] = redact_text(commit_message)

    return created_files


def solve_github_issue(repository, issue, llm_model, prompt_function, base_branch=None):
    """
    Attempt to solve a GitHub issue by modifying a single file and sending a pull-request, or
    commenting on a pull-request.

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

    from ._utilities import split_content_and_summary, text_to_json, modify_discussion, \
        remove_ansi_escape_sequences, clean_output, redact_text, Config, file_list_from_commit_message_dict, \
        ensure_images_shown, is_github_url
    from github.GithubException import GithubException
    from gitlab.exceptions import GitlabCreateError
    import traceback

    repo = Config.git_utilities.get_repository_handle(repository)

    discussion = modify_discussion(Config.git_utilities.get_conversation_on_issue(repository, issue), prompt_visionlm=prompt_function)
    print("Discussion:", discussion)

    all_files = "* " + "\n* ".join(Config.git_utilities.list_repository_files(repository))

    modifications = prompt_function(f"""
Given a list of files in the repository {repository} and a github issues description (# {issue}), determine which files need to be modified, renamed or deleted to solve the issue.
When asked to make slides or create a presentation, assume this task is a file creation.
In case the task is to analyse data, create synthetic data, or draw a plot, consider creating a notebook for this.

## Github Issue #{issue} Discussion

{discussion}

## All files in the repository

{all_files}

## Your task
Decide which of these files need to be modified, created, downloaded, renamed, copied, deleted or painted to solve #{issue} ? 
Downloads are necessary, if there is a url in the discussion and the linked file is needed in the proposed code.
Paintings should only be done if the user explicitly asks to "paint" a picture or "draw" a comic.
Do NOT create new paintings if you already created them during the discussion.
If the user asks for executing a notebook, consider this as modification.
Keep the list of actions minimal.
Response format:
- For modifications: {{"action": "modify", "filename": "..."}}
- For creations: {{"action": "create", "filename": "..."}}
- For downloads: {{"action": "download", "source_url": "...", "target_filename": "..."}}
- For renames: {{"action": "rename", "old_filename": "...", "new_filename": "..."}}
- For copies: {{"action": "copy", "old_filename": "...", "new_filename": "..."}}
- For deletions: {{"action": "delete", "filename": "..."}}
- For paintings: {{"action": "paint", "filename": "..."}}
Respond with the actions as JSON list.
""")

    instructions = text_to_json(modifications)

    # create a new branch
    if base_branch is None or base_branch == Config.git_utilities.get_default_branch_name(repository):
        # create a new branch
        branch_name = Config.git_utilities.create_branch(repository, parent_branch=base_branch)
        print("Created branch", branch_name)
    else:
        # continue on the current branch
        branch_name = base_branch
        print("Continue working on branch", branch_name)

    # sort instructions by action: downloads first, then the rest in original order
    print("unsorted instructions", instructions)
    instructions = sorted(instructions, key=lambda x: x.get('action') != 'download')
    print("sorted instructions", instructions)

    errors = []
    commit_messages = {}
    for instruction in instructions:
        action = instruction.get('action')

        for filename_key in ["filename", "new_filename", "old_filename", "target_filename"]:
            if filename_key in instruction.keys():
                filename = instruction[filename_key]
                if ".github" in filename or ".gitlab" in filename:
                    errors.append(f"Error processing {filename}: Modifying workflow files is not allowed.")
                    continue

        try:
            if action == 'create' or action == 'modify':
                filename = instruction['filename'].strip("/")

                created_files = create_or_modify_file(repository, issue, filename, branch_name, discussion,
                                                                      prompt_function)
                for filename, commit_message in created_files.items():
                    commit_messages[filename] = commit_message
            elif action == 'download':
                source_url = instruction['source_url']
                url_type = is_github_url(source_url)
                if url_type in ["image", "data"]:
                    source_url = source_url.replace("/blob/", "/raw/")
                    target_filename = instruction['target_filename'].strip("/")
                    Config.git_utilities.download_to_repository(repository, branch_name, source_url, target_filename)
                    commit_messages[target_filename] = f"Downloaded {source_url}, saved as {target_filename}."
                # else: otherwise we have it already in the text
            elif action == 'rename':
                old_filename = instruction['old_filename'].strip("/")
                new_filename = instruction['new_filename'].strip("/")
                Config.git_utilities.rename_file_in_repository(repository, branch_name, old_filename, new_filename)
                commit_messages[new_filename] = f"Renamed {old_filename} to {new_filename}."
            elif action == 'delete':
                filename = instruction['filename'].strip("/")
                Config.git_utilities.delete_file_from_repository(repository, branch_name, filename)
                commit_messages[filename] = f"Deleted {filename}."
            elif action == 'copy':
                old_filename = instruction['old_filename'].strip("/")
                new_filename = instruction['new_filename'].strip("/")
                Config.git_utilities.copy_file_in_repository(repository, branch_name, old_filename, new_filename)
                commit_messages[new_filename] = f"Copied {old_filename} to {new_filename}."
            elif action == "paint":
                filename = instruction['filename'].strip("/")
                imagen_prompt = prompt_function("From the following discussion, extract a prompt to paint a picture as discussed:\n\n" + discussion + "\n\nNow extract a prompt for painting a picture as discussed:")
                commit_messages[filename] = paint_picture(repository, branch_name, prompt=imagen_prompt, output_filename=filename)

        except Exception as e:
            traces = "    " + remove_ansi_escape_sequences(traceback.format_exc()).replace("\n", "\n    ")
            summary = f"""<details>
    <summary>Error during {instruction}: {e}</summary>
    <pre>{traces}</pre>
</details>
            """
            errors.append(summary)

    error_messages = ""
    if len(errors) > 0:
        error_messages = "\n\nDuring solving this task, the following errors occurred:\n\n* " + "\n* ".join(
            errors) + "\n"

    print(error_messages)

    # get a diff of all changes
    diffs_prompt = Config.git_utilities.get_diff_of_branches(repository, branch_name, base_branch=base_branch)

    # summarize the changes
    commit_messages_prompt = "* " + "\n* ".join([f"{k}: {v}" for k,v in commit_messages.items()])

    file_list = file_list_from_commit_message_dict(repository, branch_name, commit_messages)
    file_list_text = ""
    for md_link in file_list:
        if md_link.startswith("!"):
            file_list_text = file_list_text + "* " + md_link[1:] + " <explanation>\n\n" + md_link + "\n\n"
        else:
            file_list_text = file_list_text + "* " + md_link + " <explanation>\n\n"

    from ._utilities import Config
    remark = setup_ai_remark() + "\n\n"

    if branch_name != base_branch:

        pull_request_summary = prompt_function(f"""
{SYSTEM_PROMPT}
Given a Github issue description, a list of commit messages, a git diff and a list of mark-down links, summarize the changes you made in the files.
Add the list of markdown links but replace <explanation> with a single sentence describing what was changed in the respective file. Keep the list as it is otherwise.
You modified the repository {repository} to solve the issue #{issue}, which is also summarized below.

## Github Issue #{issue} Discussion

{discussion}

## Commit messages
You committed these changes to these files

{commit_messages_prompt}

## Git diffs
The following changes were made in the files:

{diffs_prompt}

## List of links

{file_list_text}

## Your task

Summarize the changes above to a one paragraph which will be Github pull-request message. 
Write the message as if you were a human talking to a human.
Below add the list of markdown links but replace <explanation> with a single sentence describing what was changed in the respective file. Keep the list as it is otherwise.

Afterwards, summarize the summary in a single line, which will become the title of the pull-request.
Do not add headlines or any other formatting. Just respond with the paragraph, the list of markdown links with explanations and the title in a new line below.
""")


        pull_request_description, pull_request_title = split_content_and_summary(pull_request_summary)

        pull_request_description = ensure_images_shown(pull_request_description, file_list)
        pull_request_description = pull_request_description.replace("\n* ![", "\n![")

        full_report = remark + clean_output(repository, pull_request_description) + error_messages

        try:
            Config.git_utilities.send_pull_request(repository,
                          source_branch=branch_name,
                          target_branch=base_branch,
                          title=redact_text(pull_request_title),
                          description=redact_text(full_report) + f"\n\ncloses #{issue}")
        except GithubException as e:
            Config.git_utilities.add_comment_to_issue(repository, issue, f"{remark}Error creating pull-request: {e}{error_messages}")
        except GitlabCreateError as e:
            Config.git_utilities.add_comment_to_issue(repository, issue, f"{remark}Error creating pull-request: {e}{error_messages}")

    else:
        modification_summary = prompt_function(f"""
{SYSTEM_PROMPT}
Given a Github issue description, a list of commit messages, and a list of mark-down links, summarize the changes you made in the files.
Add the list of markdown links but replace <explanation> with a single sentence describing what was changed in the respective file.
## Github Issue #{issue} Discussion
{discussion}
## Commit messages
You committed these changes to these files
{commit_messages_prompt}
## List of links
{file_list_text}
## Your task
Summarize the changes above to a one paragraph. Write your response as if you were a human talking to a human.
Below add the list of markdown links but replace <explanation> with a single sentence describing what was changed in the respective file.
Do not add headline or any other formatting. Just respond with the paragraphe below.
""")

        modification_summary = ensure_images_shown(modification_summary, file_list)

        Config.git_utilities.add_comment_to_issue(repository, issue, remark + redact_text(clean_output(repository, modification_summary)) + redact_text(error_messages))


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
    from ._utilities import text_to_json, Config
    from ._github_utilities import create_issue

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

        issue_number = create_issue(repository, title, ai_remark + body)
        sub_issue_numbers.append(issue_number)

        if len(created_sub_tasks) == 0:
            created_sub_tasks = "## Other sub-tasks\nThe following sub-tasks have already been identified:\n"
        created_sub_tasks += f"### {title}\n{body}\n\n"

    # Create a comment on the main issue with the list of sub-issues
    sub_issue_links = "\n".join([f"- #{num}" for num in sub_issue_numbers])
    comment_text = f"Sub-issues have been created:\n{sub_issue_links}"
    Config.git_utilities.add_comment_to_issue(repository, issue, ai_remark + comment_text)

    return sub_issue_numbers

def paint_picture(repository, branch_name, prompt, output_filename="image.png", model="dall-e-3", image_width=1024, image_height=1024, style='vivid', quality='standard'):
    """Generate an image using DALL-E3 based on a prompt and save it to the repository using PIL."""
    Log().log(f"-> paint_image({repository}, {branch_name}, ..., {output_filename}, {model}, ...)")
    from openai import OpenAI
    import io
    from ._utilities import images_from_url_responses, Config
    client = OpenAI()

    size_str = f"{image_width}x{image_height}"

    kwargs = {}
    if model == "dall-e-3":
        kwargs['style'] = style
        kwargs['quality'] = quality

    response = client.images.generate(
        prompt=prompt,
        n=1,
        model=model,
        size=size_str,
        **kwargs
    )

    image = images_from_url_responses(response)

    # convert to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # commit
    commit_message = "Painted image"
    Config.git_utilities.write_file_in_branch(repository, branch_name, output_filename, img_byte_arr, commit_message=commit_message)

    return commit_message
