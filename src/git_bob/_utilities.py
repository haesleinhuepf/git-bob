def remove_indentation(text):
    """
    Remove leading indentation from a block of text.

    Parameters
    ----------
    text : str
        The text from which to remove indentation.

    Returns
    -------
    str
        The text with leading indentation removed.
    """
    lines = text.split('\n')
    indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    return '\n'.join(line[indent:] for line in lines)


def remove_outer_markdown(text):
    """
    Remove outer markdown from a block of text.

    Parameters
    ----------
    text : str
        The text from which to remove outer markdown.

    Returns
    -------
    str
        The text with outer markdown removed.
    """
    if text.startswith("```") and text.endswith("```"):
        return text[3:-3].strip()
    return text
