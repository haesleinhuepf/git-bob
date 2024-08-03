def faculty(number):
    """
    Calculate the factorial of a number.

    Parameters
    ----------
    number : int
        The number to calculate the factorial for.

    Returns
    -------
    int
        The factorial of the input number.
    """
    if number == 0:
        return 1
    else:
        return number * faculty(number - 1)

for i in range(10):
    print("The faculty of", i, "is", faculty(i))