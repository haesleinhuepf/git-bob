import os
import re
from pathlib import Path


def find_git_root(path='.'):
    """
    Find the root directory of a Git repository.

    Parameters
    ----------
    path : str, optional
        The starting path to search from. Default is the current directory ('.').

    Returns
    -------
    str or None
        The path to the root directory of the Git repository if found, None otherwise.

    Notes
    -----
    This function searches for a '.git' directory by traversing up the directory tree.
    """
    path = Path(path).resolve()
    for p in [path, *path.parents]:
        if (p / '.git').is_dir():
            return str(p)
    return None


def find_files(directory, pattern):
    """
    Find files in a directory that match a given pattern.

    Parameters
    ----------
    directory : str
        The directory to search in.
    pattern : str
        The regex pattern to match filenames against.

    Returns
    -------
    list of str
        A list of file paths that match the given pattern.

    Notes
    -----
    This function uses os.walk to recursively search the directory and its subdirectories.
    """
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if re.match(pattern, filename):
                matches.append(os.path.join(root, filename))
    return matches


def remove_prefix(text, prefix):
    """
    Remove a prefix from a string if it exists.

    Parameters
    ----------
    text : str
        The input string.
    prefix : str
        The prefix to remove.

    Returns
    -------
    str
        The input string with the prefix removed if it existed, otherwise the original string.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text