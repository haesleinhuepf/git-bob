from ._ai_github_utilities.comment_on_issue import comment_on_issue
from ._ai_github_utilities.solve_issue import solve_github_issue, split_issue_in_sub_issues
from ._ai_github_utilities.comment_on_issue import setup_ai_remark
from ._ai_github_utilities.utilities import fix_error_in_notebook, review_pull_request, summarize_github_issue, create_or_modify_file, paint_picture

# Making these functions available at the module level for backward compatibility
__all__ = [
    'setup_ai_remark',
    'comment_on_issue', 
    'review_pull_request',
    'summarize_github_issue',
    'fix_error_in_notebook',
    'create_or_modify_file',
    'solve_github_issue',
    'split_issue_in_sub_issues',
    'paint_picture'
]
