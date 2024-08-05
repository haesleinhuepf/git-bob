def endpoint_function(param1, param2):
    """
    Processes the given parameters to produce a result.

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : int
        The second parameter.

    Returns
    -------
    result : int
        The sum of param1 and param2.
    """
    result = param1 + param2
    return result

def another_endpoint_function(param1, param2, flag=False):
    """
    Performs an operation based on the provided parameters and flag.

    Parameters
    ----------
    param1 : float
        The first numerical parameter.
    param2 : float
        The second numerical parameter.
    flag : bool, optional
        A flag to alter the behavior of the function, by default False.

    Returns
    -------
    result : float
        The product of param1 and param2 if flag is True, otherwise their difference.
    """
    if flag:
        result = param1 * param2
    else:
        result = param1 - param2
    return result