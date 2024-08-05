<BEGIN_FILE>
import openai
import json
from ._github_utilities import get_github_issue, get_file_content
from ._logger import logger
from ._utilities import load_config

def get_ai_response(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=None):
    """
    Get a response from the OpenAI API.

    Parameters
    ----------
    prompt : str
        The input prompt for the AI model.
    model : str, optional
        The AI model to use. Default is "gpt-3.5-turbo".
    temperature : float, optional
        Controls randomness in the output. Default is 0.7.
    max_tokens : int, optional
        The maximum number of tokens in the response. Default is None.

    Returns
    -------
    str
        The AI-generated response.

    Raises
    ------
    Exception
        If there's an error in the API call or response parsing.
    """
    config = load_config()
    openai.api_key = config["openai_api_key"]

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error in API call: {str(e)}")
        raise

def get_ai_code_review(repo, pull_request_number):
    """
    Get an AI-generated code review for a specific pull request.

    Parameters
    ----------
    repo : github.Repository.Repository
        The GitHub repository object.
    pull_request_number : int
        The number of the pull request to review.

    Returns
    -------
    str
        The AI-generated code review.

    Raises
    ------
    Exception
        If there's an error in retrieving the pull request or generating the review.
    """
    try:
        pull_request = repo.get_pull(pull_request_number)
        diff = pull_request.diff()
        
        prompt = f"Please review the following code changes and provide feedback:\n\n{diff}"
        
        return get_ai_response(prompt)
    except Exception as e:
        logger.error(f"Error in getting AI code review: {str(e)}")
        raise

def get_ai_issue_summary(repo, issue_number):
    """
    Get an AI-generated summary of a GitHub issue.

    Parameters
    ----------
    repo : github.Repository.Repository
        The GitHub repository object.
    issue_number : int
        The number of the issue to summarize.

    Returns
    -------
    str
        The AI-generated issue summary.

    Raises
    ------
    Exception
        If there's an error in retrieving the issue or generating the summary.
    """
    try:
        issue = get_github_issue(repo, issue_number)
        
        prompt = f"Please summarize the following GitHub issue:\n\nTitle: {issue.title}\n\nBody: {issue.body}"
        
        return get_ai_response(prompt)
    except Exception as e:
        logger.error(f"Error in getting AI issue summary: {str(e)}")
        raise

def get_ai_code_suggestion(repo, issue_number):
    """
    Get an AI-generated code suggestion for a specific GitHub issue.

    Parameters
    ----------
    repo : github.Repository.Repository
        The GitHub repository object.
    issue_number : int
        The number of the issue to generate a code suggestion for.

    Returns
    -------
    str
        The AI-generated code suggestion.

    Raises
    ------
    Exception
        If there's an error in retrieving the issue or generating the suggestion.
    """
    try:
        issue = get_github_issue(repo, issue_number)
        
        prompt = f"Based on the following GitHub issue, please suggest a code solution:\n\nTitle: {issue.title}\n\nBody: {issue.body}"
        
        return get_ai_response(prompt)
    except Exception as e:
        logger.error(f"Error in getting AI code suggestion: {str(e)}")
        raise
</END_FILE>
