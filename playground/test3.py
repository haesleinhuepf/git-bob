def sum_of_squares(numbers):
    """
    Calculate the sum of squares of a list of numbers.

    Parameters
    ----------
    numbers : list of int or float
        List of numbers to be squared and summed.

    Returns
    -------
    int or float
        The sum of the squares of the numbers.
    """
    return sum([n**2 for n in numbers])


def print_sum_of_squares(numbers):
    """
    Print the sum of squares of a list of numbers.

    Parameters
    ----------
    numbers : list of int or float
        List of numbers to be squared and summed.
    """
    print(f"Sum of squares of {numbers} is {sum_of_squares(numbers)}")