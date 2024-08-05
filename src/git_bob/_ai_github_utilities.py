"""
Utilities for interacting with GitHub API.
"""
import json
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from github import Github
from github.GithubException import GithubException
from github.Repository import Repository


def get_github_repo(
    owner: str, repo_name: str, token: Optional[str] = None
) -> Repository:
    """
    Get a GitHub repository object.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo_name : str
        The name of the repository.
    token : str, optional
        The GitHub access token. If None, uses the environment variable
        `GITHUB_TOKEN`.

    Returns
    -------
    Repository
        The GitHub repository object.

    Raises
    ------
    GithubException
        If the repository is not found or the access token is invalid.
    """
    if token is None:
        token = os.getenv("GITHUB_TOKEN")
    if token is None:
        raise ValueError("GitHub access token is required.")
    github = Github(token)
    return github.get_repo(f"{owner}/{repo_name}")


def create_github_issue(
    repo: Repository,
    title: str,
    body: str,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
) -> None:
    """
    Create a new issue in a GitHub repository.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    title : str
        The title of the issue.
    body : str
        The body of the issue.
    labels : List[str], optional
        A list of labels to apply to the issue.
    assignees : List[str], optional
        A list of users to assign the issue to.

    Raises
    ------
    GithubException
        If the issue creation fails.
    """
    repo.create_issue(title=title, body=body, labels=labels, assignees=assignees)


def get_github_issue_comments(repo: Repository, issue_number: int) -> List[Dict[str, Any]]:
    """
    Get all comments for a given issue.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    issue_number : int
        The issue number.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries, each representing a comment.

    Raises
    ------
    GithubException
        If the issue is not found or the access token is invalid.
    """
    issue = repo.get_issue(number=issue_number)
    comments = issue.get_comments()
    return [comment.raw_data for comment in comments]


def create_github_issue_comment(
    repo: Repository, issue_number: int, body: str
) -> None:
    """
    Create a new comment on a given issue.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    issue_number : int
        The issue number.
    body : str
        The body of the comment.

    Raises
    ------
    GithubException
        If the issue is not found or the access token is invalid.
    """
    issue = repo.get_issue(number=issue_number)
    issue.create_comment(body)


def get_github_pull_request(
    repo: Repository, pr_number: int
) -> Dict[str, Any]:
    """
    Get a GitHub pull request object.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.

    Returns
    -------
    Dict[str, Any]
        The GitHub pull request object.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    return pr.raw_data


def get_github_pull_request_commits(
    repo: Repository, pr_number: int
) -> List[Dict[str, Any]]:
    """
    Get all commits for a given pull request.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries, each representing a commit.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    commits = pr.get_commits()
    return [commit.raw_data for commit in commits]


def get_github_pull_request_files(
    repo: Repository, pr_number: int
) -> List[Dict[str, Any]]:
    """
    Get all files for a given pull request.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries, each representing a file.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    files = pr.get_files()
    return [file.raw_data for file in files]


def get_github_pull_request_reviews(
    repo: Repository, pr_number: int
) -> List[Dict[str, Any]]:
    """
    Get all reviews for a given pull request.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries, each representing a review.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    reviews = pr.get_reviews()
    return [review.raw_data for review in reviews]


def get_github_pull_request_review_comments(
    repo: Repository, pr_number: int
) -> List[Dict[str, Any]]:
    """
    Get all review comments for a given pull request.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries, each representing a review comment.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    comments = pr.get_review_comments()
    return [comment.raw_data for comment in comments]


def create_github_pull_request_review(
    repo: Repository, pr_number: int, body: str, event: str, comments: List[Dict[str, Any]]
) -> None:
    """
    Create a new review for a given pull request.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.
    body : str
        The body of the review.
    event : str
        The event of the review.
    comments : List[Dict[str, Any]]
        A list of review comments.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    pr.create_review(body=body, event=event, comments=comments)


def get_github_pull_request_merge_status(repo: Repository, pr_number: int) -> str:
    """
    Get the merge status of a given pull request.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.

    Returns
    -------
    str
        The merge status of the pull request.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    return pr.mergeable_state


def merge_github_pull_request(repo: Repository, pr_number: int) -> None:
    """
    Merge a given pull request.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    pr_number : int
        The pull request number.

    Raises
    ------
    GithubException
        If the pull request is not found or the access token is invalid.
    """
    pr = repo.get_pull(number=pr_number)
    pr.merge()


def get_github_branch_protection(repo: Repository, branch_name: str) -> Dict[str, Any]:
    """
    Get the branch protection settings for a given branch.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    branch_name : str
        The name of the branch.

    Returns
    -------
    Dict[str, Any]
        The branch protection settings.

    Raises
    ------
    GithubException
        If the branch is not found or the access token is invalid.
    """
    protection = repo.get_branch(branch_name).get_protection()
    return protection.raw_data


def update_github_branch_protection(
    repo: Repository, branch_name: str, protection_rules: Dict[str, Any]
) -> None:
    """
    Update the branch protection settings for a given branch.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    branch_name : str
        The name of the branch.
    protection_rules : Dict[str, Any]
        The branch protection settings to update.

    Raises
    ------
    GithubException
        If the branch is not found or the access token is invalid.
    """
    branch = repo.get_branch(branch_name)
    protection = branch.get_protection()
    protection.update(protection_rules)


def get_github_branch_protection_rules(repo: Repository, branch_name: str) -> List[Dict[str, Any]]:
    """
    Get the branch protection rules for a given branch.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    branch_name : str
        The name of the branch.

    Returns
    -------
    List[Dict[str, Any]]
        The branch protection rules.

    Raises
    ------
    GithubException
        If the branch is not found or the access token is invalid.
    """
    protection = repo.get_branch(branch_name).get_protection()
    return protection.raw_data["required_status_checks"]["contexts"]


def update_github_branch_protection_rules(
    repo: Repository, branch_name: str, protection_rules: List[Dict[str, Any]]
) -> None:
    """
    Update the branch protection rules for a given branch.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    branch_name : str
        The name of the branch.
    protection_rules : List[Dict[str, Any]]
        The branch protection rules to update.

    Raises
    ------
    GithubException
        If the branch is not found or the access token is invalid.
    """
    branch = repo.get_branch(branch_name)
    protection = branch.get_protection()
    protection.update({"required_status_checks": {"contexts": protection_rules}})


def get_github_workflow_runs(
    repo: Repository, workflow_id: int, status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get the workflow runs for a given workflow.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    workflow_id : int
        The workflow ID.
    status : str, optional
        The status of the workflow runs to filter by.

    Returns
    -------
    List[Dict[str, Any]]
        The workflow runs.

    Raises
    ------
    GithubException
        If the workflow is not found or the access token is invalid.
    """
    runs = repo.get_workflow(workflow_id).get_runs()
    if status is not None:
        runs = [run for run in runs if run.status == status]
    return [run.raw_data for run in runs]


def get_github_workflow_run_logs(
    repo: Repository, workflow_id: int, run_id: int
) -> str:
    """
    Get the logs for a given workflow run.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    workflow_id : int
        The workflow ID.
    run_id : int
        The run ID.

    Returns
    -------
    str
        The workflow run logs.

    Raises
    ------
    GithubException
        If the workflow run is not found or the access token is invalid.
    """
    run = repo.get_workflow(workflow_id).get_run(run_id)
    return run.get_logs()


def get_github_workflow_run_jobs(
    repo: Repository, workflow_id: int, run_id: int
) -> List[Dict[str, Any]]:
    """
    Get the jobs for a given workflow run.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    workflow_id : int
        The workflow ID.
    run_id : int
        The run ID.

    Returns
    -------
    List[Dict[str, Any]]
        The jobs for the workflow run.

    Raises
    ------
    GithubException
        If the workflow run is not found or the access token is invalid.
    """
    run = repo.get_workflow(workflow_id).get_run(run_id)
    return [job.raw_data for job in run.get_jobs()]


def get_github_workflow_run_job_logs(
    repo: Repository, workflow_id: int, run_id: int, job_id: int
) -> str:
    """
    Get the logs for a given workflow run job.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    workflow_id : int
        The workflow ID.
    run_id : int
        The run ID.
    job_id : int
        The job ID.

    Returns
    -------
    str
        The workflow run job logs.

    Raises
    ------
    GithubException
        If the workflow run job is not found or the access token is invalid.
    """
    job = repo.get_workflow(workflow_id).get_run(run_id).get_job(job_id)
    return job.get_logs()


def get_github_workflow_run_job_steps(
    repo: Repository, workflow_id: int, run_id: int, job_id: int
) -> List[Dict[str, Any]]:
    """
    Get the steps for a given workflow run job.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    workflow_id : int
        The workflow ID.
    run_id : int
        The run ID.
    job_id : int
        The job ID.

    Returns
    -------
    List[Dict[str, Any]]
        The steps for the workflow run job.

    Raises
    ------
    GithubException
        If the workflow run job is not found or the access token is invalid.
    """
    job = repo.get_workflow(workflow_id).get_run(run_id).get_job(job_id)
    return [step.raw_data for step in job.get_steps()]


def get_github_workflow_run_job_step_logs(
    repo: Repository, workflow_id: int, run_id: int, job_id: int, step_number: int
) -> str:
    """
    Get the logs for a given workflow run job step.

    Parameters
    ----------
    repo : Repository
        The GitHub repository object.
    workflow_id : int
        The workflow ID.
    run_id : int
        The run ID.
    job_id : int
        The job ID.
    step_number : int
        The step number.

    Returns
    -------
    str
        The workflow run job step logs.

    Raises
    ------
    GithubException
        If the workflow run job step is not found or the access token is invalid.
    """
    job = repo.get_workflow(workflow_id).get_run(run_id).get_job(job_id)
    step = job.get_steps()[step_number]
    return step.get_logs()