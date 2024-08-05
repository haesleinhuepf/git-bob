<BEGIN_FILE>
import re
from typing import List

from ._github_utilities import (
    get_issue_number_from_github_references,
    get_pull_request_body,
    get_pull_request_number_from_github_references,
)

def extract_issue_number_from_branch_name(branch_name: str) -> int:
    """
    Extract the issue number from a branch name.

    Parameters
    ----------
    branch_name : str
        The name of the branch.

    Returns
    -------
    int
        The extracted issue number.

    Raises
    ------
    ValueError
        If no issue number is found in the branch name.
    """
    match = re.search(r'(\d+)', branch_name)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"No issue number found in branch name: {branch_name}")

def extract_issue_numbers_from_commit_message(commit_message: str) -> List[int]:
    """
    Extract issue numbers from a commit message.

    Parameters
    ----------
    commit_message : str
        The commit message to extract issue numbers from.

    Returns
    -------
    List[int]
        A list of extracted issue numbers.
    """
    return get_issue_number_from_github_references(commit_message)

def extract_pull_request_number_from_branch_name(branch_name: str) -> int:
    """
    Extract the pull request number from a branch name.

    Parameters
    ----------
    branch_name : str
        The name of the branch.

    Returns
    -------
    int
        The extracted pull request number.

    Raises
    ------
    ValueError
        If no pull request number is found in the branch name.
    """
    match = re.search(r'pr-(\d+)', branch_name)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"No pull request number found in branch name: {branch_name}")

def extract_pull_request_numbers_from_commit_message(commit_message: str) -> List[int]:
    """
    Extract pull request numbers from a commit message.

    Parameters
    ----------
    commit_message : str
        The commit message to extract pull request numbers from.

    Returns
    -------
    List[int]
        A list of extracted pull request numbers.
    """
    return get_pull_request_number_from_github_references(commit_message)

def extract_pull_request_body(pull_request_number: int) -> str:
    """
    Extract the body of a pull request.

    Parameters
    ----------
    pull_request_number : int
        The number of the pull request.

    Returns
    -------
    str
        The body of the pull request.
    """
    return get_pull_request_body(pull_request_number)
</END_FILE>
