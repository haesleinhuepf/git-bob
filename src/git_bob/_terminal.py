def command_line_interface():
    import os
    import sys

    from ._github_utilities import comment_on_issue, get_conversation_on_issue, get_most_recent_comment_on_issue
    from ._endpoints import prompt_claude, prompt_chatgpt

    print("Hello")
    # Read the environment variable "ANTHROPIC_API_KEY"
    if os.environ.get("ANTHROPIC_API_KEY") is not None:
        print("Using claude...")
        prompt = prompt_claude
    elif os.environ.get("OPENAI_API_KEY") is not None:
        print("Using gpt...")
        prompt = prompt_chatgpt
    else:
        raise NotImplementedError("No API key specified.")

    # Print out all arguments passed to the script
    print("Script arguments:")
    for arg in sys.argv[1:]:
        print(arg)

    task = sys.argv[1]
    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None

    system_prompt = """You are an extremely skilled python developer."""

    user, text = get_most_recent_comment_on_issue(repository, issue)
    remark = "<sup>This comment was generated by [git-bob](https://github.com/haesleinhuepf/git-bob), an AI-based assistant.</sup>"

    if ("git-bob comment" in text or "git-bob solve" in text) and remark not in text:

        discussion = get_conversation_on_issue(repository, issue)

        print("Discussion:", discussion)

        if task == "review-pull-request":
            # load temp.txt into a variable
            with open("temp.txt", "r") as file:
                file_changes = file.read()

            print("file_changes:", file_changes)

            comment = prompt(f"""
{system_prompt}
Generate a response to a github pull-request. 
Given are the discussion on the pull-request and the changed files.

## Discussion

{discussion}

## Change files

{file_changes}

## Your task

Respond to the discussion above. 
Do NOT explain your response or anything else. 
Just respond to the discussion.
""")

            print("comment:", comment)

            comment_on_issue(repository, issue, f"""        
{remark}

---
{comment}
""")
        elif task == "comment-on-issue" and "git-bob solve" in text:
            from ._github_utilities import solve_github_issue
            solve_github_issue(repository, issue)
        elif task == "comment-on-issue" and "git-bob comment" in text:
            comment = prompt(f"""
{system_prompt}
Respond to a github issue. Its entire discussion is given.

## Discussion

{discussion}

## Your task

Respond to the discussion above. 
Do NOT explain your response or anything else. 
Just respond to the discussion.
""")

            print("comment:", comment)

            comment_on_issue(repository, issue, f"""        
{remark}

---
{comment}
""")
