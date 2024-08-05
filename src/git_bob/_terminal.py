import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown

def execute_command(command):
    """
    Execute a shell command and return its output.

    Parameters
    ----------
    command : str
        The shell command to execute.

    Returns
    -------
    str
        The output of the executed command.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

def print_pretty(text, syntax="python"):
    """
    Print text with syntax highlighting.

    Parameters
    ----------
    text : str
        The text to print.
    syntax : str, optional
        The syntax highlighting to use (default is "python").
    """
    console = Console()
    syntax = Syntax(text, syntax, theme="monokai", line_numbers=True)
    console.print(syntax)

def print_markdown(text):
    """
    Print text as formatted markdown.

    Parameters
    ----------
    text : str
        The markdown text to print.
    """
    console = Console()
    md = Markdown(text)
    console.print(md)

def print_panel(text, title=""):
    """
    Print text in a panel.

    Parameters
    ----------
    text : str
        The text to print in the panel.
    title : str, optional
        The title of the panel (default is "").
    """
    console = Console()
    panel = Panel(text, title=title)
    console.print(panel)

def get_user_input(prompt):
    """
    Get user input with a prompt.

    Parameters
    ----------
    prompt : str
        The prompt to display to the user.

    Returns
    -------
    str
        The user's input.
    """
    return input(prompt)

def print_error(message):
    """
    Print an error message.

    Parameters
    ----------
    message : str
        The error message to print.
    """
    console = Console(stderr=True)
    console.print(f"[bold red]Error:[/bold red] {message}", file=sys.stderr)