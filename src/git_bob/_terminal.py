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
    from ._github_utilities import check_access_and_ask_for_approval, get_github_repository, get_most_recently_commented_issue
    from ._utilities import quick_first_response, Config, deploy
    from ._logger import Log
    from github.GithubException import UnknownObjectException
    from ._utilities import run_cli

    print("Hello")

    # read environment variables
    timeout_in_seconds = os.environ.get("TIMEOUT_IN_SECONDS", 900) # 15 minutes
    Config.llm_name = os.environ.get("GIT_BOB_LLM_NAME", "gpt-4o-2024-08-06")
    Config.run_id = os.environ.get("GITHUB_RUN_ID", None)

    agent_name = os.environ.get("GIT_BOB_AGENT_NAME", "git-bob")

    from git_bob import __version__
    Log().log(f"I am {agent_name} " + str(__version__))

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
    if issue is None:
        issue = get_most_recently_commented_issue(repository)

    user, text = get_most_recent_comment_on_issue(repository, issue)
    text = text.lower()

    print("text: ", text)
    print(f"{agent_name} ask in text", f"{agent_name} ask" in text)

    # handle ask-llm task option
    if f"{agent_name} ask" in text:
        print("Dynamic LLM selection")
        new_llm_name = text.split(f"{agent_name} ask")[-1].strip().split(" ")[0]
        if "gemini" in new_llm_name or "github_models" in new_llm_name or "claude" in new_llm_name or "gpt" in new_llm_name:
            Config.llm_name = new_llm_name
        text = text.replace(f"{agent_name} ask {new_llm_name} to ", f"{agent_name} ")
        # example:
        # git-bob ask gpt-4o to solve this issue -> git-bob solve this issue

    if "github_models:" in Config.llm_name and os.environ.get("GH_MODELS_API_KEY") is not None:
        prompt = prompt_azure
    elif "kisski:" in Config.llm_name and os.environ.get("KISSKI_API_KEY") is not None:
        prompt = partial(prompt_chatgpt, base_url="https://chat-ai.academiccloud.de/v1", api_key=os.environ.get("KISSKI_API_KEY"))
    elif "blablador:" in Config.llm_name and os.environ.get("BLABLADOR_API_KEY") is not None:
        prompt = partial(prompt_chatgpt, base_url="https://helmholtz-blablador.fz-juelich.de:8000/v1", api_key=os.environ.get("BLABLADOR_API_KEY"))
    elif "claude" in Config.llm_name and os.environ.get("ANTHROPIC_API_KEY") is not None:
        prompt = prompt_claude
    elif "gpt" in Config.llm_name and os.environ.get("OPENAI_API_KEY") is not None:
        prompt = prompt_chatgpt
    elif "gemini" in Config.llm_name and os.environ.get("GOOGLE_API_KEY") is not None:
        prompt = prompt_gemini
    else:
        llm_name = Config.llm_name[1:]
        raise NotImplementedError(f"Make sure to specify the environment variables GIT_BOB_LLM_NAME and corresponding API KEYs (setting:_{llm_name}).")
    Log().log("Using language model: _" + Config.llm_name[1:])

    text = text.replace(f"{agent_name}, ", f"{agent_name} ")
    
    # aliases for comment action
    text = text.replace(f"{agent_name} respond", f"{agent_name} comment")
    text = text.replace(f"{agent_name} review", f"{agent_name} comment")
    text = text.replace(f"{agent_name} think about", f"{agent_name} comment")

    # aliases for solve action
    text = text.replace(f"{agent_name} implement", f"{agent_name} solve")
    text = text.replace(f"{agent_name} apply", f"{agent_name} solve")

    # determine task to do
    if running_in_github_ci:
        if not (f"{agent_name} comment" in text or f"{agent_name} solve" in text or f"{agent_name} split" in text or f"{agent_name} deploy" in text):
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
            text = text + f"\n{agent_name} comment"
        elif task == "solve-issue":
            text = text + f"\n{agent_name} solve"
        elif task == "split-issue":
            text = text + f"\n{agent_name} split"
        else:
            raise NotImplementedError(f"Unknown task '{task}'. I show myself out.")

    # thumbs up for quick response
    quick_first_response(repository, issue)

    # determine if it is a PR
    repo = get_github_repository(repository)
    try:
        pull_request = repo.get_pull(issue)
        base_branch = pull_request.head.ref
        print("Issue is a a PR - switching to the branch", base_branch)
        run_cli("git fetch --all", verbose=True)
        run_cli(f"git checkout -b {base_branch} origin/{base_branch}", verbose=True)

        # Extract source (head) and target (base) branches
        base_branch = pull_request.head.ref
        #target_branch = pull_request.base.ref
    except UnknownObjectException:
        print("Issue is a not a PR")
        pull_request = None
        base_branch = repo.default_branch

    # execute the task
    if f"{agent_name} comment" in text:
        if pull_request is not None:
            review_pull_request(repository, issue, prompt)
        else:
            comment_on_issue(repository, issue, prompt)
    elif f"{agent_name} split" in text:
        split_issue_in_sub_issues(repository, issue, prompt)
    elif f"{agent_name} solve" in text:
        # could be issue or modifying code in a PR
        solve_github_issue(repository, issue, Config.llm_name, prompt, base_branch=base_branch)
    elif f"{agent_name} deploy" in text:
        deploy(repository, issue)
    else:
        raise NotImplementedError(f"Unknown task. I show myself out.")

    print("Done. Summary:")
    print("* " + "\n* ".join(Log().get()))
