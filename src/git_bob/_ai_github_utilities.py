# for backwards compatibility

from ._utilities import AGENT_NAME, SYSTEM_PROMPT, setup_ai_remark
from .default_agent import comment_on_issue
from .default_agent import review_pull_request
from .default_agent import solve_github_issue, try_to_solve_github_issue, create_or_modify_file, fix_error_in_notebook
from .default_agent import split_issue_in_sub_issues

