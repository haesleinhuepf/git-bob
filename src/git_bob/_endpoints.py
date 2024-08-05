from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from git_bob.auth import get_current_user
from git_bob.db import (
    get_db,
    add_repository,
    delete_repository,
    get_repository,
    get_repositories,
    update_repository,
)
from git_bob.models import Repository, User

router = APIRouter(prefix="/repos", tags=["repositories"])


class RepositoryCreate(BaseModel):
    name: str
    url: str
    description: Optional[str] = None


class RepositoryUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


@router.get("/", response_model=List[Repository])
async def get_repositories(
    current_user: User = Depends(get_current_user),
    db: Any = Depends(get_db),
) -> List[Repository]:
    """
    Get a list of repositories for the current user.

    Parameters
    ----------
    current_user : User
        The current user.
    db : Any
        The database connection.

    Returns
    -------
    List[Repository]
        A list of repositories.
    """
    return get_repositories(db, current_user.id)


@router.post("/", response_model=Repository)
async def create_repository(
    repository: RepositoryCreate,
    current_user: User = Depends(get_current_user),
    db: Any = Depends(get_db),
) -> Repository:
    """
    Create a new repository.

    Parameters
    ----------
    repository : RepositoryCreate
        The repository data.
    current_user : User
        The current user.
    db : Any
        The database connection.

    Returns
    -------
    Repository
        The created repository.
    """
    return add_repository(db, repository, current_user.id)


@router.get("/{repo_id}", response_model=Repository)
async def get_repository_by_id(
    repo_id: int,
    current_user: User = Depends(get_current_user),
    db: Any = Depends(get_db),
) -> Repository:
    """
    Get a repository by ID.

    Parameters
    ----------
    repo_id : int
        The ID of the repository.
    current_user : User
        The current user.
    db : Any
        The database connection.

    Returns
    -------
    Repository
        The repository.

    Raises
    ------
    HTTPException
        If the repository is not found.
    """
    repository = get_repository(db, repo_id)
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repository


@router.put("/{repo_id}", response_model=Repository)
async def update_repository_by_id(
    repo_id: int,
    repository: RepositoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Any = Depends(get_db),
) -> Repository:
    """
    Update a repository by ID.

    Parameters
    ----------
    repo_id : int
        The ID of the repository.
    repository : RepositoryUpdate
        The updated repository data.
    current_user : User
        The current user.
    db : Any
        The database connection.

    Returns
    -------
    Repository
        The updated repository.

    Raises
    ------
    HTTPException
        If the repository is not found.
    """
    repository = get_repository(db, repo_id)
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    return update_repository(db, repo_id, repository)


@router.delete("/{repo_id}")
async def delete_repository_by_id(
    repo_id: int,
    current_user: User = Depends(get_current_user),
    db: Any = Depends(get_db),
) -> JSONResponse:
    """
    Delete a repository by ID.

    Parameters
    ----------
    repo_id : int
        The ID of the repository.
    current_user : User
        The current user.
    db : Any
        The database connection.

    Returns
    -------
    JSONResponse
        A success message.

    Raises
    ------
    HTTPException
        If the repository is not found.
    """
    repository = get_repository(db, repo_id)
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    delete_repository(db, repo_id)
    return JSONResponse(content={"message": "Repository deleted successfully"})