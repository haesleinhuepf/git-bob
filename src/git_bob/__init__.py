def add(a, b):
    """
    Add two numbers.

    Parameters
    ----------
    a : int or float
        The first number.
    b : int or float
        The second number.

    Returns
    -------
    int or float
        The sum of the two numbers.
    """
    return a + b


def subtract(a, b):
    """
    Subtract second number from the first number.

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
    """
    return a - b


def multiply(a, b):
    """
    Multiply two numbers.

    Parameters
    ----------
    a : int or float
        The first number.
    b : int or float
        The second number.

    Returns
    -------
    int or float
        The product of the two numbers.
    """
    return a * b


def divide(a, b):
    """
    Divide the first number by the second number.

    Parameters
    ----------
    a : int or float
        The dividend.
    b : int or float
        The divisor.

    Returns
    -------
    int or float
        The quotient of the division.

    Raises
    ------
    ZeroDivisionError
        If the divisor is zero.
    """
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b