"""
Module for terminal related functions.
"""
import os
import sys
from typing import List, Union

def get_terminal_size(fallback: Union[List[int], None] = None) -> List[int]:
    """
    Get the terminal size.

    Parameters
    ----------
    fallback : Union[List[int], None], optional
        Fallback value if the terminal size cannot be determined, by default None

    Returns
    -------
    List[int]
        A list containing the width and height of the terminal.
        If the terminal size cannot be determined, returns the fallback value.
    """
    try:
        columns, rows = os.get_terminal_size()
        return [columns, rows]
    except OSError:
        if fallback:
            return fallback
        else:
            return [80, 24]

def clear_terminal() -> None:
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width() -> int:
    """
    Get the terminal width.

    Returns
    -------
    int
        The width of the terminal.
    """
    return get_terminal_size()[0]

def get_terminal_height() -> int:
    """
    Get the terminal height.

    Returns
    -------
    int
        The height of the terminal.
    """
    return get_terminal_size()[1]

def print_centered(text: str, width: int = None) -> None:
    """
    Prints a string centered on the terminal.

    Parameters
    ----------
    text : str
        The string to be printed.
    width : int, optional
        The width of the terminal, by default None
    """
    if width is None:
        width = get_terminal_width()
    padding = (width - len(text)) // 2
    print(" " * padding + text)

def print_title(text: str, width: int = None, char: str = "-") -> None:
    """
    Prints a title with a line of characters above and below it.

    Parameters
    ----------
    text : str
        The title text.
    width : int, optional
        The width of the terminal, by default None
    char : str, optional
        The character to use for the line, by default "-"
    """
    if width is None:
        width = get_terminal_width()
    print(char * width)
    print_centered(text, width)
    print(char * width)

def print_error(text: str) -> None:
    """
    Prints an error message in red.

    Parameters
    ----------
    text : str
        The error message.
    """
    print("\033[91m" + text + "\033[0m")

def print_warning(text: str) -> None:
    """
    Prints a warning message in yellow.

    Parameters
    ----------
    text : str
        The warning message.
    """
    print("\033[93m" + text + "\033[0m")

def print_success(text: str) -> None:
    """
    Prints a success message in green.

    Parameters
    ----------
    text : str
        The success message.
    """
    print("\033[92m" + text + "\033[0m")

def print_info(text: str) -> None:
    """
    Prints an info message in blue.

    Parameters
    ----------
    text : str
        The info message.
    """
    print("\033[94m" + text + "\033[0m")

def print_progress_bar(progress: float, width: int = 50) -> None:
    """
    Prints a progress bar.

    Parameters
    ----------
    progress : float
        The progress of the task, between 0 and 1.
    width : int, optional
        The width of the progress bar, by default 50
    """
    filled_blocks = int(progress * width)
    empty_blocks = width - filled_blocks
    bar = "[" + "#" * filled_blocks + " " * empty_blocks + "]"
    percentage = int(progress * 100)
    print(f"\r{bar} {percentage}%", end="")
    sys.stdout.flush()