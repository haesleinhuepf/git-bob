def get_author_from_commit(commit: str) -> str:
  """Extracts author from a commit hash.

  Parameters
  ----------
  commit : str
    A commit hash.

  Returns
  -------
  str
    Author of the commit.

  Raises
  ------
  ValueError
    If the commit hash is not a valid hash.
  """
  try:
    author = subprocess.check_output(
        ["git", "show", "-s", "--pretty=format:%an", commit]
    ).decode("utf-8").strip()
  except subprocess.CalledProcessError:
    raise ValueError(f"Invalid commit hash: {commit}")
  return author