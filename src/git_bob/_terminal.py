# This module provides the command line interface for interacting with GitHub issues and pull requests.
# It supports functionalities such as reviewing pull requests, solving issues, and commenting on issues
# using AI models like GPT and Claude. The script can be run in a GitHub CI environment with a timeout.

def command_line_interface():
    import os 
    import sys
    import signal

    from ._github_utilities import get_most_recent_comment_on_issue, add_comment_to_issue
    from ._ai_github_utilities import setup_ai_remark, solve_github_issue, review_pull_request, comment_on_issue, split_issue_in_sub_issues
    from ._github_utilities import check_access_and_ask_for_approval, get_repository_handle, get_most_recently_commented_issue
    from ._utilities import quick_first_response, Config, deploy 
    from ._logger import Log
    from github.GithubException import UnknownObjectException
    from ._utilities import run_cli
    import inspect

    print("Hello")

    # read environment variables
    timeout_in_seconds = os.environ.get("TIMEOUT_IN_SECONDS", 900) # 15 minutes
    Config.llm_name = os.environ.get("GIT_BOB_LLM_NAME", "gpt-4o-2024-08-06")
    Config.run_id = os.environ.get("GITHUB_RUN_ID", None)
    Config.git_server_url = os.environ.get("GIT_SERVER_URL", "https://github.com/")
    if "https://github.com" in Config.git_server_url:
        import git_bob._github_utilities as gu
        Config.git_utilities = gu
        print("Using gitHUB utilities")
    else:
        import git_bob._gitlab_utilities as gu
        Config.git_utilities = gu
        print("Using gitLAB utilities")

    agent_name = os.environ.get("GIT_BOB_AGENT_NAME", "git-bob")

    from git_bob import __version__
    Log().log(f"I am {agent_name} " + str(__version__))
    Log().log(f"Accessing {Config.git_server_url}")

    # initialize prompt handlers
    prompt_handlers = init_prompt_handlers()

    # determine values for aliases
    model_aliases = {}
    for key, value in prompt_handlers.items():
        if value is not None:
            try:
                signature = inspect.signature(value)
                model_aliases[key] = signature.parameters['model'].default
            except:
                continue
    print("model aliases:\n", model_aliases)

    available_handlers = {}
    for key, value in prompt_handlers.items():
        if value is not None:
            available_handlers[key] = value
    print("Available prompt handlers:", ", ".join([p.replace(":","") for p in list(available_handlers.keys())]))

    # Print out all arguments passed to the script
    print("Script arguments:")
    for arg in sys.argv[1:]:
        print(arg)

    task = sys.argv[1]

    # test if we're running in the github-CI
    Config.running_in_github_ci = task.endswith("-action") and "https://github.com" in Config.git_server_url
    Config.running_in_gitlab_ci = task.endswith("-action") and not "https://github.com" in Config.git_server_url
    task = task.replace("-action", "")

    # setting timeout
    if Config.running_in_github_ci or Config.running_in_gitlab_ci:
        print(f"Running in CI. Setting timeout to {timeout_in_seconds / 60} minutes.")
        # in case we run in the github-CI, we set a timeout
        def handler(signum, frame):
            print("Process timed out")
            sys.exit(1)
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout_in_seconds)  # Set the timeout to 3 minutes

    # determine need to respond and access rights
    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue_str = sys.argv[3] if len(sys.argv) > 3 else None
    if issue_str is not None and issue_str.startswith("!"):
        print("It's a gitlab merge request!")
        Config.is_pull_request = True
        pull_request = int(issue_str)
        issue_str = issue_str[1:]
    else:
        pull_request = None
        Config.is_pull_request = False
    issue = int(issue_str) if len(sys.argv) > 3 else None
    if issue is None:
        # todo: remove this and fail here instead https://github.com/haesleinhuepf/git-bob/issues/385
        issue = Config.git_utilities.get_most_recently_commented_issue(repository)

    Config.repository = repository
    Config.issue = issue

    user, text = Config.git_utilities.get_most_recent_comment_on_issue(repository, issue)
    text = text.lower()

    print("text: ", text)
    print(f"{agent_name} ask in text", f"{agent_name} ask" in text)

    # handle ask-llm task option
    if f"{agent_name} ask" in text:
        # example:
        # git-bob ask gpt-4o to solve this issue -> git-bob solve this issue
        print("Dynamic LLM selection")
        new_llm_name = text.split(f"{agent_name} ask")[-1].strip().split(" ")[0]
        text = text.replace(f"{agent_name} ask {new_llm_name} to ", f"{agent_name} ")

        # Apply model alias if it exists
        if new_llm_name in model_aliases:
            new_llm_name  = model_aliases[new_llm_name]
        for key in prompt_handlers:
            if key in new_llm_name:
                Config.llm_name = new_llm_name
                break


    prompt = None
    prompt_handlers = init_prompt_handlers() # reinitialize, because configured LLM may have changed
    for key, value in prompt_handlers.items():
        if key in Config.llm_name and value.api_key is not None:
            prompt = value.prompt_function
            break

    if prompt is None:
        llm_name = Config.llm_name[1:]
        raise NotImplementedError(f"Make sure to specify the environment variables GIT_BOB_LLM_NAME and corresponding API KEYs (llm_name:_{llm_name}).")
    Log().log("Using language model: _" + Config.llm_name[1:])

    text = text.replace(f"{agent_name}, ", f"{agent_name} ")
    text = text.replace(f"{agent_name} please ", f"{agent_name} ")
    
    # aliases for comment action
    text = text.replace(f"{agent_name} respond", f"{agent_name} comment")
    #text = text.replace(f"{agent_name} review", f"{agent_name} comment")
    text = text.replace(f"{agent_name} think about", f"{agent_name} comment")
    text = text.replace(f"{agent_name} answer", f"{agent_name} comment")

    # aliases for solve action
    text = text.replace(f"{agent_name} implement", f"{agent_name} solve")
    text = text.replace(f"{agent_name} apply", f"{agent_name} solve")

    # determine task to do
    if Config.running_in_github_ci or Config.running_in_gitlab_ci:
        if not (f"{agent_name} comment" in text or f"{agent_name} review" in text or f"{agent_name} solve" in text or f"{agent_name} try" in text or f"{agent_name} split" in text or f"{agent_name} deploy" in text):
            print("They didn't speak to me. I show myself out:", text)
            sys.exit(0)
        ai_remark = setup_ai_remark()
        if ai_remark in text:
            print("No need to respond to myself. I show myself out.")
            sys.exit(0)
        if not Config.git_utilities.check_access_and_ask_for_approval(user, repository, issue):
            sys.exit(1)
    else:
        # when running from terminal (e.g. for development), we modify the text to include the command from the terminal
        if task == "comment-on-issue":
            text = text + f"\n{agent_name} comment"
        elif task == "solve-issue":
            text = text + f"\n{agent_name} solve"
        elif task == "try-issue":
            text = text + f"\n{agent_name} try"
        elif task == "split-issue":
            text = text + f"\n{agent_name} split"
        else:
            raise NotImplementedError(f"Unknown task '{task}'. I show myself out.")

    # thumbs up for quick response
    quick_first_response(repository, issue)

    # determine if it is a PR
    if Config.running_in_github_ci:
        repo = Config.git_utilities.get_repository_handle(repository)
        try:
            Config.pull_request = repo.get_pull(issue)
            base_branch = Config.pull_request.head.ref
            print("Issue is a a PR - switching to the branch", base_branch)
            run_cli("git fetch --all", verbose=True)
            run_cli(f"git checkout -b {base_branch} origin/{base_branch}", verbose=True)

            # Extract source (head) and target (base) branches
            #base_branch = Config.pull_request.head.ref
            #target_branch = Config.pull_request.base.ref
        except UnknownObjectException:
            print("Issue is a not a PR")
            Config.pull_request = None
            base_branch = repo.default_branch
    elif Config.running_in_gitlab_ci:
        base_branch = Config.git_utilities.get_default_branch_name(repository)
    else:
        base_branch = "main"

    # execute the task
    if f"{agent_name} review" in text and Config.pull_request is not None:
        review_pull_request(repository, issue, prompt)
    elif f"{agent_name} comment" in text or  f"{agent_name} review" in text: # fallback to comment
        comment_on_issue(repository, issue, prompt)
    elif f"{agent_name} split" in text:
        split_issue_in_sub_issues(repository, issue, prompt)
    elif f"{agent_name} solve" in text or f"{agent_name} try" in text:
        if f"{agent_name} try" in text:
            target_branch = Config.git_utilities.create_branch(repository, base_branch)
        else:
            target_branch = base_branch
        # could be issue or modifying code in a PR
        solve_github_issue(repository, issue, Config.llm_name, prompt, base_branch=target_branch)
    elif f"{agent_name} deploy" in text:
        deploy(repository, issue)
    else:
        raise NotImplementedError(f"Unknown task. I show myself out.")

    print("Done. Summary:")
    print("* " + "\n* ".join(Log().get()))

def init_prompt_handlers():
    """Initialize and return prompt handlers from entry points.

    Returns
    -------
    dict
        Dictionary mapping handler names to functions that can handle prompts
    """
    from importlib.metadata import entry_points
    
    handlers = {}
    for entry_point in entry_points(group='git_bob.prompt_handlers'):
        try:
            handler_func = entry_point.load()
            key = entry_point.name
            handlers[key] = handler_func
        except Exception as e:
            print(f"Failed to load handler {entry_point.name}: {e}")
    
    return handlers

def remote_interface():
    """
    Advanced remote interaction interface for handling GitHub repositories.

    Extracts the repository and issue number from command-line arguments, creates a temporary
    directory, clones the repository, and invokes the command line interface for further actions.
    """
    import os
    import sys
    import tempfile

    from ._utilities import run_cli

    # Extract repository and issue number from sys.argv
    task = sys.argv[1] if len(sys.argv) > 1 else None
    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue_number = sys.argv[3] if len(sys.argv) > 3 else None

    if task not in ["comment-on-issue", "solve-issue", "try-issue", "split-issue"]:
        print("Invalid task. Must be comment-on-issue, solve-issue, try-issue or split-issue Exiting.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname) # Switch to temporary directory

        # Execute git clone command
        run_cli(f"git clone https://github.com/{repository}", verbose=True)

        # Extract the repository name from the full repository path
        repo_name = repository.rsplit('/', 1)[1].replace('.git', '')

        # Switch to the cloned repository directory
        os.chdir(tmpdirname + "/" + repo_name)

        # Call the command line interface function
        command_line_interface()
