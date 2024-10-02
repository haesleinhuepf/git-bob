# This module provides the command line interface for interacting with GitHub issues and pull requests.
# It supports functionalities such as reviewing pull requests, solving issues, and commenting on issues
# using AI models like GPT and Claude. The script can be run in a GitHub CI environment with a timeout.

def command_line_interface():
    import os
    import sys
    import signal

    from ._github_utilities import get_most_recent_comment_on_issue, add_comment_to_issue
    from ._ai_github_utilities import setup_ai_remark, solve_github_issue, review_pull_request, comment_on_issue, split_issue_in_sub_issues
    from ._endpoints import prompt_claude, prompt_chatgpt, prompt_gemini, prompt_azure
    from ._github_utilities import check_access_and_ask_for_approval, get_github_repository
    from ._utilities import get_llm_name, quick_first_response
    from ._logger import Log
    from github.GithubException import UnknownObjectException

    print("Hello")

    # read environment variables
    timeout_in_seconds = os.environ.get("TIMEOUT_IN_SECONDS", 900) # 15 minutes
    llm_name = get_llm_name()
    if "github_models:" in llm_name and os.environ.get("GH_MODELS_API_KEY") is not None:
        prompt = prompt_azure
    elif "claude" in llm_name and os.environ.get("ANTHROPIC_API_KEY") is not None:
        prompt = prompt_claude
    elif "gpt" in llm_name and os.environ.get("OPENAI_API_KEY") is not None:
        prompt = prompt_chatgpt
    elif "gemini" in llm_name and os.environ.get("GOOGLE_API_KEY") is not None:
        prompt = prompt_gemini
    else:
        raise NotImplementedError("Make sure to specify the environment variables GIT_BOB_LLM_NAME and corresponding API KEYs.")

    from git_bob import __version__
    Log().log("I am git-bob " + str(__version__))
    Log().log("Using language model: " + llm_name)

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
            print("Process timed out")
            sys.exit(1)
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout_in_seconds)  # Set the timeout to 3 minutes

    # determine need to respond and access rights
    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None
    user, text = get_most_recent_comment_on_issue(repository, issue)

    # handle aliases
    text = text.replace("gitbob", "gib-bob") # typing - on the phone is hard
    text = text.replace("git-bob respond", "git-bob comment")
    text = text.replace("git-bob review", "git-bob comment")
    text = text.replace("git-bob think about", "git-bob comment")
    text = text.replace("git-bob implement", "git-bob solve")

    if running_in_github_ci:
        if not ("git-bob comment" in text or "git-bob solve" in text or "git-bob split" in text):
            print("They didn't speak to me. I show myself out.")
            sys.exit(0)
        ai_remark = setup_ai_remark()
        if ai_remark in text:
            print("No need to respond to myself. I show myself out.")
            sys.exit(0)
        if not check_access_and_ask_for_approval(user, repository, issue):
            sys.exit(1)

    quick_first_response()

    repo = get_github_repository(repository)
    try:
        pull_request = repo.get_pull(issue)
        print("Issue is a a PR")

        # Extract source (head) and target (base) branches
        base_branch = pull_request.head.ref
        #target_branch = pull_request.base.ref
    except UnknownObjectException:
        print("Issue is a not a PR")
        base_branch = repo.default_branch

    # execute the task
    if task == "review-pull-request":
        review_pull_request(repository, issue, prompt)
    elif ((not running_in_github_ci and task == "solve-issue") or
          (running_in_github_ci and task == "comment-on-issue" and "git-bob solve" in text)):
        solve_github_issue(repository, issue, llm_name, prompt, base_branch=base_branch)
    elif ((task == "comment-on-issue" and "git-bob split" in text) or (task == "split-issue" and not running_in_github_ci)):
        split_issue_in_sub_issues(repository, issue, prompt)
    elif task == "comment-on-issue" and ("git-bob comment" in text or not running_in_github_ci):
        comment_on_issue(repository, issue, prompt)
    else:
        raise NotImplementedError("Unknown task. I show myself out.")

    print("Done. Summary:")
    print("* " + "\n* ".join(Log().get()))
