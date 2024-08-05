from typing import List, Dict, Any, Tuple
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import git
import os
from git_bob._git_utils import get_repo, get_changed_files, commit_changes
from git_bob._prompts import get_system_prompt, get_user_prompt
from git_bob._llm import get_completion

app = FastAPI()

class SolveRequest(BaseModel):
    issue_number: int
    repo_path: str

class ReviewRequest(BaseModel):
    pr_number: int
    repo_path: str

@app.post("/solve")
async def solve_issue(request: SolveRequest) -> Dict[str, Any]:
    """
    Solve a GitHub issue.

    Parameters
    ----------
    request : SolveRequest
        The request object containing the issue number and repository path.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the solution details.

    Raises
    ------
    HTTPException
        If there's an error during the solving process.
    """
    try:
        repo = get_repo(request.repo_path)
        issue = repo.get_issue(request.issue_number)
        
        system_prompt = get_system_prompt()
        user_prompt = get_user_prompt(issue)
        
        completion = get_completion(system_prompt, user_prompt)
        
        changed_files = get_changed_files(completion)
        
        commit_message = f"Solve issue #{request.issue_number}"
        commit_sha = commit_changes(repo, changed_files, commit_message)
        
        return {"success": True, "commit_sha": commit_sha}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review")
async def review_pr(request: ReviewRequest) -> Dict[str, Any]:
    """
    Review a GitHub pull request.

    Parameters
    ----------
    request : ReviewRequest
        The request object containing the pull request number and repository path.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the review details.

    Raises
    ------
    HTTPException
        If there's an error during the review process.
    """
    try:
        repo = get_repo(request.repo_path)
        pr = repo.get_pull(request.pr_number)
        
        system_prompt = get_system_prompt()
        user_prompt = get_user_prompt(pr)
        
        completion = get_completion(system_prompt, user_prompt)
        
        pr.create_review(body=completion, event='COMMENT')
        
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))