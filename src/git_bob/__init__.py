"""
This module provides functionalities for the git-bob project.
"""

def example_function(param1, param2):
    """
    An example function that illustrates how to write docstrings.
    
    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str
        The second parameter, which is a string.

    Returns
    -------
    bool
        The return value. True for success, False otherwise.
    """
    return isinstance(param1, int) and isinstance(param2, str)

def add(a, b):
    """
    Adds two numbers.
    
    Parameters
    ----------
    a : int or float
        The first number.
    b : int or float
        The second number.

    Returns
    -------
    int or float
        The sum of `a` and `b`.
    """
    return a + b

def multiply(a, b):
    """
    Multiplies two numbers.
    
    Parameters
    ----------
    a : int or float
        The first number.
    b : int or float
        The second number.

    Returns
    -------
    int or float
        The product of `a` and `b`.
    """
    return a * b