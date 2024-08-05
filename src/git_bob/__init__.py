<BEGIN_FILE>
"""
Git-bob: An AI-powered GitHub assistant.

This module provides functionality for interacting with GitHub repositories
and performing AI-assisted tasks.
"""

from ._ai_github_utilities import (
    create_issue_from_text,
    create_pull_request_from_text,
    update_issue_from_text,
    update_pull_request_from_text,
)
from ._github_utilities import (
    get_issue,
    get_pull_request,
    get_repository,
    get_user,
    list_issues,
    list_pull_requests,
)
from ._terminal import (
    print_issue,
    print_issues,
    print_pull_request,
    print_pull_requests,
)

__all__ = [
    "create_issue_from_text",
    "create_pull_request_from_text",
    "update_issue_from_text",
    "update_pull_request_from_text",
    "get_issue",
    "get_pull_request",
    "get_repository",
    "get_user",
    "list_issues",
    "list_pull_requests",
    "print_issue",
    "print_issues",
    "print_pull_request",
    "print_pull_requests",
]
</END_FILE>
