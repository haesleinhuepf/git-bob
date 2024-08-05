def add(a, b):
    """
    Add two numbers.

    Parameters
    ----------
    a : int or float
        First number to add.
    b : int or float
        Second number to add.

    Returns
    -------
    int or float
        The sum of a and b.
    """
    return a + b

def subtract(a, b):
    """
    Subtract second number from first number.

    Parameters
    ----------
    a : int or float
        Number from which to subtract.
    b : int or float
        Number to subtract.

    Returns
    -------
    int or float
        The result of a minus b.
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers.

    Parameters
    ----------
    a : int or float
        First number to multiply.
    b : int or float
        Second number to multiply.

    Returns
    -------
    int or float
        The product of a and b.
    """
    return a * b

def divide(a, b):
    """
    Divide first number by second number.

    Parameters
    ----------
    a : int or float
        Numerator.
    b : int or float
        Denominator.

    Returns
    -------
    int or float
        The quotient of a divided by b.

    Raises
    ------
    ZeroDivisionError
        If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b