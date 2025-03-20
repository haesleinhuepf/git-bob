def deploy(repository, issue, **kwargs):
    """
    Deploy the package to PyPI.

    Parameters
    ----------
    repository: str
        The repository name.
    issue: str
        The issue number where to post the deployment report.
    """
    from .._utilities import run_cli, Config, setup_ai_remark, remove_ansi_escape_sequences
    #from ._github_utilities import add_comment_to_issue
    result1 = run_cli("python setup.py sdist bdist_wheel")
    result2 = run_cli("twine upload dist/*")
    Config.git_utilities.add_comment_to_issue(repository, issue, setup_ai_remark() + remove_ansi_escape_sequences(f"\n# Deployment report\n\n{result1}\n{result2}"))
