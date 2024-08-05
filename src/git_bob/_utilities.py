def add(a, b):
    """
    Add two numbers.

    Parameters
    ----------
    a : int or float
        The first number to add.
    b : int or float
        The second number to add.

    Returns
    -------
    int or float
        The sum of the two numbers.

    Examples
    --------
    >>> add(2, 3)
    5
    >>> add(1.5, 2.5)
    4.0
    """
    return a + b


def subtract(a, b):
    """
    Subtract one number from another.

    Parameters
    ----------
    a : int or float
        The number to be subtracted from.
    b : int or float
        The number to subtract.

    Returns
    -------
    int or float
        The result of the subtraction.

    Examples
    --------
    >>> subtract(5, 3)
    2
    >>> subtract(2.5, 1.5)
    1.0
    """
    return a - b


def multiply(a, b):
    """
    Multiply two numbers.

    Parameters
    ----------
    a : int or float
        The first number to multiply.
    b : int or float
        The second number to multiply.

    Returns
    -------
    int or float
        The product of the two numbers.

    Examples
    --------
    >>> multiply(2, 3)
    6
    >>> multiply(1.5, 2)
    3.0
    """
    return a * b


def divide(a, b):
    """
    Divide one number by another.

    Parameters
    ----------
    a : int or float
        The number to be divided.
    b : int or float
        The number to divide by.

    Returns
    -------
    float
        The result of the division.

    Raises
    ------
    ZeroDivisionError
        If `b` is zero.

    Examples
    --------
    >>> divide(6, 3)
    2.0
    >>> divide(7.5, 2.5)
    3.0
    """
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b