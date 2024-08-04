"""
This module provides helper functions to interact with different language models.

Functions:
- prompt_claude: Sends a message to the Claude language model and returns the text response.
- prompt_chatgpt: Sends a message to the ChatGPT language model and returns the text response.
"""

def prompt_claude(message: str, model="claude-3-5-sonnet-20240620"):
    """
    A prompt helper function that sends a message to anthropic
    and returns only the text response.

    Parameters
    ----------
    message : str
        The message to send to the Claude language model.
    model : str, optional
        The model to use for the Claude language model. Default is "claude-3-5-sonnet-20240620".

    Returns
    -------
    str
        The text response from the Claude language model.

    Example
    -------
    >>> prompt_claude("Hello, Claude!")
    'Hello! How can I assist you today?'

    Example models: claude-3-5-sonnet-20240620 or claude-3-opus-20240229
    """
    from anthropic import Anthropic

    # convert message in the right format if necessary
    if isinstance(message, str):
        message = [{"role": "user", "content": message}]

    # setup connection to the LLM
    client = Anthropic()

    message = client.messages.create(
        max_tokens=4096,
        messages=message,
        model=model,
    )

    # extract answer
    return message.content[0].text


def prompt_chatgpt(message: str, model="gpt-4o-2024-05-13"):
    """
    A prompt helper function that sends a message to openAI
    and returns only the text response.

    Parameters
    ----------
    message : str
        The message to send to the ChatGPT language model.
    model : str, optional
        The model to use for the ChatGPT language model. Default is "gpt-4o-2024-05-13".

    Returns
    -------
    str
        The text response from the ChatGPT language model.

    Example
    -------
    >>> prompt_chatgpt("Hello, ChatGPT!")
    'Hello! How can I assist you today?'
    """
    # convert message in the right format if necessary
    import openai
    if isinstance(message, str):
        message = [{"role": "user", "content": message}]

    # setup connection to the LLM
    client = openai.OpenAI()

    # submit prompt
    response = client.chat.completions.create(
        model=model,
        messages=message
    )

    # extract answer
    return response.choices[0].message.content
