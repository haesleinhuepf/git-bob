def sum_of_squares(numbers):
    """
    Calculate the sum of squares of a list of numbers.

    Parameters
    ----------
    numbers : list of int or float
        A list of numbers to calculate the sum of squares.

    Returns
    -------
    int or float
        The sum of squares of the numbers in the list.
    """
    return sum([n**2 for n in numbers])


def print_sum_of_squares(numbers):
    """
    Print the sum of squares of a list of numbers.

    Parameters
    ----------
    numbers : list of int or float
        A list of numbers to calculate and print the sum of squares.

    Returns
    -------
    None
    """
    print(f"Sum of squares of {numbers} is {sum_of_squares(numbers)}")