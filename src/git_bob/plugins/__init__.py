class PromptHandler:
    def __init__(self, api_key, prompt_function):
        self.api_key = api_key
        self.prompt_function = prompt_function

def register_handler(prompt_function, api_key_entry, base_url=None):
    """Register a prompt handler with the given parameters.
    
    Parameters
    ----------
    prompt_function : callable
        The function that handles the prompt request
    api_key_entry : str
        Environment variable name containing the API key
    base_url : str, optional
        Base URL for the API endpoint
        
    Returns
    -------
    PromptHandler
        Configured prompt handler instance
    """
    return PromptHandler(
        api_key=os.environ.get(api_key_entry),
        prompt_function=partial(prompt_function, base_url=base_url, api_key=os.environ.get(api_key_entry))
    )
