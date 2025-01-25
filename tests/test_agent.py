def test_agent_comment_on_issue():
    import os
    from git_bob import _github_utilities
    from git_bob._utilities import Config
    from git_bob._github_utilities import create_issue, get_most_recent_comment_on_issue, close_issue
    from git_bob._ai_github_utilities import comment_on_issue
    from git_bob._endpoints import prompt_azure

    Config.repository  = "haesleinhuepf/git-bob"
    Config.issue = create_issue(Config.repository, "for-loops", "git-bob answer with python code for demonstrating a for-loop that outputs numbers between 0 and 10.")

    os.environ["GIT_BOB_LLM_NAME"] = "gh_models:gpt-4o"
    Config.is_pull_request = False
    Config.git_server_url = "https://github.com/"
    Config.llm_name = "gpt-4o"
    Config.running_in_github_ci = True
    Config.git_utilities = _github_utilities

    _, former_comment = get_most_recent_comment_on_issue(Config.repository, Config.issue)

    comment_on_issue(Config.repository, Config.issue, prompt_azure)

    _, new_comment = get_most_recent_comment_on_issue(Config.repository, Config.issue)

    close_issue(Config.repository, Config.issue)

    print(new_comment)

    assert former_comment != new_comment
    assert "print" in new_comment

