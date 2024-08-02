def command_line_interface():
    import os
    import sys

    from ._github_utilities import get_most_recent_comment_on_issue
    from ._ai_github_utilities import setup_ai_remark, solve_github_issue, review_pull_request, comment_on_issue
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

    # test if we're running in the github-CI
    running_in_github_ci = task.endswith("-action")
    task = task.replace("-action", "")

    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None

    user, text = get_most_recent_comment_on_issue(repository, issue)

    ai_remark = setup_ai_remark()

    if not running_in_github_ci or (("git-bob comment" in text or "git-bob solve" in text) and ai_remark not in text):
        if task == "review-pull-request":
            review_pull_request(repository, issue, prompt)
        elif (not running_in_github_ci and task == "solve-issue") or (task == "comment-on-issue" and "git-bob solve" in text):
            solve_github_issue(repository, issue)
        elif task == "comment-on-issue" and ("git-bob comment" in text or not running_in_github_ci):
            comment_on_issue(repository, issue, prompt)
