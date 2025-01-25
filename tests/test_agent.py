import pytest

def test_agent_comment_on_issue():
    import os
    from functools import partial
    from git_bob import _github_utilities
    from git_bob._utilities import Config
    from git_bob._github_utilities import create_issue, get_most_recent_comment_on_issue, close_issue
    from git_bob._ai_github_utilities import comment_on_issue
    from git_bob._endpoints import prompt_azure

    Config.repository  = "haesleinhuepf/git-bob"
    Config.issue = create_issue(Config.repository, "for-loops", "git-bob answer with python code for demonstrating a for-loop that outputs numbers between 0 and 10.")

    os.environ["GIT_BOB_LLM_NAME"] = "gh_models:gpt-4o-mini"
    Config.is_pull_request = False
    Config.git_server_url = "https://github.com/"
    Config.llm_name = "gpt-4o-mini"
    Config.running_in_github_ci = True
    Config.git_utilities = _github_utilities
    prompt_azure = partial(prompt_azure, model=Config.llm_name)

    _, former_comment = get_most_recent_comment_on_issue(Config.repository, Config.issue)

    comment_on_issue(Config.repository, Config.issue, prompt_azure)

    _, new_comment = get_most_recent_comment_on_issue(Config.repository, Config.issue)

    close_issue(Config.repository, Config.issue)

    print(new_comment)

    assert former_comment != new_comment
    assert "print" in new_comment

@pytest.mark.manual
def test_agent_try_solving_issue():
    import os
    from functools import partial
    from git_bob import _github_utilities
    from git_bob._utilities import Config
    from git_bob._github_utilities import create_issue, get_most_recent_comment_on_issue, close_issue
    from git_bob._ai_github_utilities import try_to_solve_github_issue
    from git_bob._endpoints import prompt_azure

    Config.repository  = "haesleinhuepf/git-bob"
    Config.issue = create_issue(Config.repository, "for-loops", "git-bob try python code for demonstrating a for-loop that outputs numbers between 0 and 10.")

    os.environ["GIT_BOB_LLM_NAME"] = "gh_models:gpt-4o-mini"
    Config.is_pull_request = False
    Config.git_server_url = "https://github.com/"
    Config.llm_name = "gpt-4o-mini"
    Config.running_in_github_ci = True
    Config.git_utilities = _github_utilities
    prompt_azure = partial(prompt_azure, model=Config.llm_name)

    _, former_comment = get_most_recent_comment_on_issue(Config.repository, Config.issue)

    try_to_solve_github_issue(Config.repository, Config.issue, prompt_azure, "main")

    _, new_comment = get_most_recent_comment_on_issue(Config.repository, Config.issue)

    close_issue(Config.repository, Config.issue)

    print(new_comment)

    assert former_comment != new_comment



def test_agent_solving_issue():
    import os
    from functools import partial
    from git_bob import _github_utilities
    from git_bob._utilities import Config
    from git_bob._github_utilities import create_issue, get_most_recent_comment_on_issue, close_issue
    from git_bob._ai_github_utilities import solve_github_issue, review_pull_request
    from git_bob._endpoints import prompt_azure

    Config.repository  = "haesleinhuepf/git-bob"
    Config.issue = create_issue(Config.repository, "for-loops", "git-bob implement python code in a new 'for_loop.py' that demonstrates a for-loop that outputs numbers between 0 and 10.")

    os.environ["GIT_BOB_LLM_NAME"] = "gh_models:gpt-4o-mini"
    Config.is_pull_request = False
    Config.git_server_url = "https://github.com/"
    Config.llm_name = "gpt-4o-mini"
    Config.running_in_github_ci = True
    Config.git_utilities = _github_utilities

    prompt_azure = partial(prompt_azure, model=Config.llm_name)

    _, former_comment = get_most_recent_comment_on_issue(Config.repository, Config.issue)

    message = solve_github_issue(Config.repository, Config.issue, prompt_azure, "main")
    print(message)
    pr_number = int(message.split("/")[-1])

    _, pr_message = get_most_recent_comment_on_issue(Config.repository, pr_number)
    print(pr_message)

    review_pull_request(Config.repository, pr_number, prompt_azure)

    _, new_pr_message = get_most_recent_comment_on_issue(Config.repository, pr_number)

    close_issue(Config.repository, Config.issue)
    close_issue(Config.repository, pr_number)


    assert pr_number > 0
    assert f"closes #{Config.issue}" in pr_message

    assert new_pr_message != pr_message

