# This module provides the command line interface for interacting with GitHub issues and pull requests.
# It supports functionalities such as reviewing pull requests, solving issues, and commenting on issues
# using AI models like GPT and Claude. The script can be run in a GitHub CI environment with a timeout.

def command_line_interface():
    """
    Command line interface for interacting with GitHub issues and pull requests.

    This function reads environment variables, determines the task to be executed,
    and performs actions such as reviewing pull requests, solving issues, and commenting
    on issues using AI models like GPT and Claude.

    Raises
    ------
    NotImplementedError
        If the required environment variables or API keys are not set, or if solving issues
        using Claude is attempted.
    """
    import os
    import sys
    import signal

    from ._github_utilities import get_most_recent_comment_on_issue, add_comment_to_issue
    from ._ai_github_utilities import setup_ai_remark, solve_github_issue, review_pull_request, comment_on_issue
    from ._endpoints import prompt_claude, prompt_chatgpt
    from ._github_utilities import check_access_and_ask_for_approval
    from ._utilities import get_llm_name
    
    print("Hello")

    # read environment variables
    timeout_in_seconds = os.environ.get("TIMEOUT_IN_SECONDS", 300) # 5 minutes
    llm_name = get_llm_name()
    if "claude" in llm_name and os.environ.get("ANTHROPIC_API_KEY") is not None:
        print("Using claude...")
        prompt = prompt_claude
    elif "gpt" in llm_name and os.environ.get("OPENAI_API_KEY") is not None:
        print("Using gpt...")
        prompt = prompt_chatgpt
    else:
        raise NotImplementedError("Make sure to specify the environment variables GIT_BOB_LLM_NAME and corresponding API KEYs.")

    # Print out all arguments passed to the script
    print("Script arguments:")
    for arg in sys.argv[1:]:
        print(arg)

    task = sys.argv[1]

    # test if we're running in the github-CI
    running_in_github_ci = task.endswith("-action")
    task = task.replace("-action", "")

    if running_in_github_ci:
        print(f"Running in GitHub-CI. Setting timeout to {timeout_in_seconds / 60} minutes.")

        # in case we run in the github-CI, we set a timeout
        def handler(signum, frame):
            """
            Handles the timeout signal.

            Parameters
            ----------
            signum : int
                The signal number.
            frame : frame object
                The current stack frame.
            """
            print("Process timed out")
            sys.exit(1)

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout_in_seconds)  # Set the timeout to 3 minutes

    # determine need to respond and access rights
    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None
    user, text = get_most_recent_comment_on_issue(repository, issue)

    # handle aliases
    text = text.replace("git-bob respond", "git-bob comment")
    text = text.replace("git-bob review", "git-bob comment")
    
    if running_in_github_ci:
        if not ("git-bob comment" in text or "git-bob solve" in text):
            print("They didn't speak to me. I show myself out.")
            sys.exit(0)
        ai_remark = setup_ai_remark()
        if ai_remark in text:
            print("No need to respond to myself. I show myself out.")
            sys.exit(0)
        if not check_access_and_ask_for_approval(user, repository, issue):
            sys.exit(1)

    # execute the task
    if task == "review-pull-request":
        review_pull_request(repository, issue, prompt)
    elif (not running_in_github_ci and task == "solve-issue") or (task == "comment-on-issue" and "git-bob solve" in text):
        if prompt == prompt_claude:
            raise NotImplementedError("Solving issues using claude is currently not supported. Please use gpt instead.")
        solve_github_issue(repository, issue, llm_name)
    elif task == "comment-on-issue" and ("git-bob comment" in text or not running_in_github_ci):
        comment_on_issue(repository, issue, prompt)
