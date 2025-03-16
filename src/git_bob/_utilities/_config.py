import os

AGENT_NAME = os.environ.get("GIT_BOB_AGENT_NAME", "git-bob")
SYSTEM_PROMPT = os.environ.get("SYSTEM_MESSAGE", f"You are an AI-based coding assistant named {AGENT_NAME}. You are an excellent Python programmer and software engineer.")

VISION_SYSTEM_MESSAGE = os.environ.get("VISION_SYSTEM_MESSAGE", "You are a AI-based vision system. You described images professionally and clearly.")

IMAGE_FILE_ENDINGS = [".jpg", ".png", ".gif", ".jpeg"]
TEXT_FILE_ENDINGS = [".txt", ".md", ".csv", ".yml", ".yaml", ".json", ".py", ".java", ".groovy", ".jython", ".md", ".markdown", ".plaintext", ".tex", ".latex", ".txt", ".csv", ".yml", ".yaml", ".json", ".py", ".svg", ".xml"]


class Config:
    llm_name = None
    run_id = None
    repository = None
    issue = None
    running_in_github_ci = None
    running_in_gitlab_ci = None
    git_server_url = "https://github.com/"
    git_utilities = None
    is_pull_request = None
    pull_request = None
    remarks = []