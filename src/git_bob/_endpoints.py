def prompt_claude(message: str, model="claude-3-5-sonnet-20240620"):
    """
    A prompt helper function that sends a message to anthropic
    and returns only the text response.

    Parameters
    ----------
    message : str
        The message to send to the model.
    model : str, optional
        The model to use for the prompt (default is "claude-3-5-sonnet-20240620").

    Returns
    -------
    str
        The text response from the model.

    Example
    -------
    >>> prompt_claude("Hello, Claude!")
    'Hello! How can I assist you today?'
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
        The message to send to the model.
    model : str, optional
        The model to use for the prompt (default is "gpt-4o-2024-05-13").

    Returns
    -------
    str
        The text response from the model.

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
