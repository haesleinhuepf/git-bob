def prompt_claude(message: str, model="claude-3-5-sonnet-20240620"):
    """
    A prompt helper function that sends a message to anthropic
    and returns only the text response.

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