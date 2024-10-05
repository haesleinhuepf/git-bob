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
    from ._utilities import quick_first_response, Config
    from ._logger import Log
    from github.GithubException import UnknownObjectException


    print("Hello")

    # read environment variables
    timeout_in_seconds = os.environ.get("TIMEOUT_IN_SECONDS", 900) # 15 minutes
    Config.llm_name = os.environ.get("GIT_BOB_LLM_NAME", "gpt-4o-2024-08-06")
    Config.run_id = os.environ.get("GITHUB_RUN_ID", None)

    from git_bob import __version__
    Log().log("I am git-bob " + str(__version__))

    # Print out all arguments passed to the script
    print("Script arguments:")
    for arg in sys.argv[1:]:
        print(arg)

    task = sys.argv[1]

    # test if we're running in the github-CI
    running_in_github_ci = task.endswith("-action")
    task = task.replace("-action", "")

    # setting timeout
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

    print("text: ", text)
    print("git-bob ask in text", "git-bob ask" in text)

    # handle aliases
    text = text.replace("gitbob", "git-bob")  # typing - on the phone is hard
    text = text.replace("Git-bob", "git-bob")  # typing - on the phone is hard

    # handle ask-llm task option
    if "git-bob ask" in text:
        print("Dynamic LLM selection")
        Config.llm_name = text.split("git-bob ask")[-1].strip().split(" ")[0]
        text = text.replace(f"git-bob ask {Config.llm_name} to ", "git-bob ")
        # example:
        # git-bob ask gpt-4o to solve this issue -> git-bob solve this issue

    if "github_models:" in Config.llm_name and os.environ.get("GH_MODELS_API_KEY") is not None:
        prompt = prompt_azure
    elif "claude" in Config.llm_name and os.environ.get("ANTHROPIC_API_KEY") is not None:
        prompt = prompt_claude
    elif "gpt" in Config.llm_name and os.environ.get("OPENAI_API_KEY") is not None:
        prompt = prompt_chatgpt
    elif "gemini" in Config.llm_name and os.environ.get("GOOGLE_API_KEY") is not None:
        prompt = prompt_gemini
    else:
        raise NotImplementedError(f"Make sure to specify the environment variables GIT_BOB_LLM_NAME and corresponding API KEYs (setting:_{Config.llm_name[1:]}).")
    Log().log("Using language model: _" + Config.llm_name[1:])

    # aliases for comment action
    text = text.replace("git-bob respond", "git-bob comment")
    text = text.replace("git-bob review", "git-bob comment")
    text = text.replace("git-bob think about", "git-bob comment")

    # aliases for solve action
    text = text.replace("git-bob implement", "git-bob solve")
    text = text.replace("git-bob apply", "git-bob solve")

    # determine task to do
    if running_in_github_ci:
        if not ("git-bob comment" in text or "git-bob solve" in text or "git-bob split" in text):
            print("They didn't speak to me. I show myself out:", text)
            sys.exit(0)
        ai_remark = setup_ai_remark()
        if ai_remark in text:
            print("No need to respond to myself. I show myself out.")
            sys.exit(0)
        if not check_access_and_ask_for_approval(user, repository, issue):
            sys.exit(1)
    else:
        # when running from terminal (e.g. for development), we modify the text to include the command from the terminal
        if task == "comment-on-issue":
            text = text + "\ngit-bob comment"
        elif task == "solve-issue":
            text = text + "\ngit-bob solve"
        elif task == "split-issue":
            text = text + "\ngit-bob split"
        else:
            raise NotImplementedError(f"Unknown task '{task}'. I show myself out.")

    # thumbs up for quick response
    quick_first_response()

    # determine if it is a PR
    repo = get_github_repository(repository)
    try:
        pull_request = repo.get_pull(issue)
        print("Issue is a a PR")

        # Extract source (head) and target (base) branches
        base_branch = pull_request.head.ref
        #target_branch = pull_request.base.ref
    except UnknownObjectException:
        print("Issue is a not a PR")
        pull_request = None
        base_branch = repo.default_branch

    # execute the task
    if "git-bob comment" in text:
        if pull_request is not None:
            review_pull_request(repository, issue, prompt)
        else:
            comment_on_issue(repository, issue, prompt)
    elif "git-bob split" in text:
        split_issue_in_sub_issues(repository, issue, prompt)
    elif "git-bob solve" in text:
        # could be issue or modifying code in a PR
        solve_github_issue(repository, issue, Config.llm_name, prompt, base_branch=base_branch)
    else:
        raise NotImplementedError(f"Unknown task. I show myself out.")

    print("Done. Summary:")
    print("* " + "\n* ".join(Log().get()))
