# This module provides utility functions for text processing, including functions to remove indentation and outer markdown from text.
import sys
from functools import lru_cache
from functools import wraps
from toolz import curry

def remove_indentation(text):
    """
    Remove indentation from the given text.

    Parameters
    ----------
    text : str
        The text from which indentation needs to be removed.

    Returns
    -------
    str
        Text without indentation.
    """
    text = text.replace("\n    ", "\n")
    return text.strip()

def remove_outer_markdown(text):
    """
    Remove outer markdown from the given text.

    Parameters
    ----------
    text : str
        The text from which outer markdown needs to be removed.

    Returns
    -------
    str
        Text without outer markdown.
    """
    code = text \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("") \
        .replace("")

    parts = code.split("
    {log}
    