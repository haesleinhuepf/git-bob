from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from git_bob._ai_github_utilities.utilities import (
    convert_text_to_markdown,
    get_issue_description,
    get_issue_number,
    get_issue_summary,
)


class IssueSolver(ABC):
    """Base class for issue solvers."""
    
    @abstractmethod
    def solve_issue(self, issue_context: dict) -> Optional[Dict[str, Any]]:
        """Solve the issue.
        
        Parameters
        ----------
        issue_context : dict
            Issue context containing information needed to solve the issue
            
        Returns
        -------
        Optional[Dict[str, Any]]
            Solution for the issue if found, None otherwise
        """
        pass


def solve_issue(issue_context: dict) -> Optional[Dict[str, Any]]:
    """Generate solution for a given issue.

    Parameters
    ----------
    issue_context : dict
        Context information about the issue

    Returns
    -------
    Optional[Dict[str, Any]]
        Solution dictionary if a solution was found, None otherwise
    """
    issue_number = get_issue_number(issue_context)
    issue_summary = get_issue_summary(issue_context)
    issue_description = get_issue_description(issue_context)

    if not issue_summary or not issue_description:
        return None

    issue_text = convert_text_to_markdown(f"{issue_summary}\n\n{issue_description}")
    
    # TODO: Add actual issue solving logic here
    return None
