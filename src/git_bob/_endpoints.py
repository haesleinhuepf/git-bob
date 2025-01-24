"""
This module provides helper functions to interact with different language models.

Functions:
- prompt_claude: Sends a message to the Claude language model and returns the text response.
- prompt_chatgpt: Sends a message to the ChatGPT language model and returns the text response.
"""
from functools import partial
import os

class PromptHandler:
    """
    A handler for language model prompts that contains the API key and prompt function.
    """
    def __init__(self, api_key, prompt_function):
        self.api_key = api_key
        self.prompt_function = prompt_function


def register_prompt_handler(prompt_function, api_key_entry):
    """
    Decorator to register a prompt handler with the given configuration.

    Parameters
    ----------
    prompt_function : callable
        The function that handles the actual prompting. These functions should have the signature
        prompt_xyz(message, model, image)
    api_key_entry : str
        Environment variable name containing the API key

    Returns
    -------
    PromptHandler
        Configured prompt handler instance
    """
    prompt_handler = PromptHandler(os.environ.get(api_key_entry), prompt_function)
    prompt_function.prompt_handler = prompt_handler
    return prompt_function


@register_prompt_handler(api_key_entry="ANTHROPIC_API_KEY")
def prompt_claude(message: str, model="claude-3-5-sonnet-20241022", image=None):
    """
    A prompt helper function that sends a message to anthropic
    and returns only the text response.

    Example models: claude-3-5-sonnet-20240620 or claude-3-opus-20240229
    """
    from anthropic import Anthropic
    from ._utilities import image_to_url
    import base64
    import numpy as np

    def encode_image(image_array):
        """
        Encode a numpy image array to base64 string.

        Parameters
        ----------
        image_array : numpy.ndarray
            A numpy array representing the image.

        Returns
        -------
        str
            Base64 encoded string of the image.
        """
        if isinstance(image_array, np.ndarray):
            return base64.b64encode(image_array.tobytes()).decode('utf-8')

    # convert message in the right format if necessary
    if image is None:
        message = [{"role": "user", "content": message}]
    else:
        encoded_image = image_to_url(image)
        message = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": message
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encoded_image
                    }
                }
            ]
        }]

    # setup connection to the LLM
    client = Anthropic()

    message = client.messages.create(
        max_tokens=8192 if "claude-3-5" in model else 4096,
        messages=message,
        model=model,
        extra_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"} if model == "claude-3-5-20240620" else None,
    )

    # extract answer
    return message.content[0].text


@register_prompt_handler(api_key_entry="OPENAI_API_KEY")
def prompt_chatgpt(message: str, model="gpt-4o-2024-08-06", image=None, max_accumulated_responses=10, max_response_tokens=16384, base_url=None, api_key=None):
    """A prompt helper function that sends a message to openAI
    and returns only the text response.
    """
    # convert message in the right format if necessary
    from ._utilities import image_to_url
    import openai
    import warnings
    from ._utilities import append_result

    if image is None:
        message = [{"role": "user", "content": message}]
    else:
        image_url = image_to_url(image)
        message = [{"role": "user", "content": [{
                    "type": "text",
                    "text": message,
                },{
                    "type": "image_url",
                    "image_url": {"url": "data:image/png;base64," + image_url}
                }]}]
    original_message = message

    if "kisski:" in model:
        model = model.replace("kisski:", "")
    if "blablador:" in model:
        model = model.replace("blablador:", "")

    # setup connection to the LLM
    if base_url is not None and api_key is not None:
        client = openai.OpenAI(base_url=base_url, api_key=api_key)
    else:
        client = openai.OpenAI()

    result = ""

    print("model", model[1:])
    print("base_url", base_url)
    print("api_key", len(api_key) if api_key is not None else 0)

    for _ in range(0, max_accumulated_responses):

        # submit prompt
        response = client.chat.completions.create(
            model=model,
            messages=message,
            max_tokens=max_response_tokens,
        )

        result = append_result(result, response.choices[0].message.content)
        print("finish_reason", response.choices[0].finish_reason)
        print("len", len(result))

        if response.choices[0].finish_reason == "length":
            message = original_message.copy()
            message.append({"role": "assistant", "content": result})
            message.append({"role": "user", "content": "Continue!"})

            warnings.warn("Long output. Continuing conversation. When generation is continued, sometimes there might be small issues on connecting the last sentence of the previous response with the first sentence of the next response. Check output carefully.")
        else:
            break

    # extract answer
    return result

@register_prompt_handler(api_key_entry="KISSKI_API_KEY")
def prompt_kisski(message: str, model=None, image=None, max_accumulated_responses=10, max_response_tokens=16384, base_url=None, api_key=None):
    if base_url is None:
        base_url = "https://chat-ai.academiccloud.de/v1"
    if api_key is None:
        api_key = os.environ.get("KISSKI_API_KEY")
    return prompt_chatgpt(message, model=model, image=image, max_accumulated_responses=max_accumulated_responses, max_response_tokens=max_response_tokens, base_url=base_url, api_key=api_key)


@register_prompt_handler(api_key_entry="BLABLADOR_API_KEY")
def prompt_blablador(message: str, model=None, image=None, max_accumulated_responses=10, max_response_tokens=16384, base_url=None, api_key=None):
    if base_url is None:
        base_url = "https://helmholtz-blablador.fz-juelich.de:8000/v1"
    if api_key is None:
        api_key = os.environ.get("BLABLADOR_API_KEY")
    return prompt_chatgpt(message, model=model, image=image, max_accumulated_responses=max_accumulated_responses, max_response_tokens=max_response_tokens, base_url=base_url, api_key=api_key)


@register_prompt_handler(api_key_entry="GOOGLE_API_KEY")
def prompt_gemini(request, model="gemini-1.5-pro-002", image=None):
    """Send a prompt to Google Gemini and return the response"""
    from google import generativeai as genai
    import os
    from ._utilities import image_to_url
    import base64
    
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    client = genai.GenerativeModel(model)
    
    if image is not None:
        response = client.generate_content([image, request])
    else:
        response = client.generate_content(request)
        
    return response.text


@register_prompt_handler(api_key_entry="GH_MODELS_API_KEY")
def prompt_azure(message: str, model="gpt-4o", image=None):
    """A prompt helper function that sends a message to Azure's OpenAI Service
    and returns only the text response.
    """
    import os
    from ._utilities import image_to_url

    token = os.environ["GH_MODELS_API_KEY"]
    endpoint = "https://models.inference.ai.azure.com"
    model = model.replace("github_models:", "")

    if "gpt" not in model and "o1" not in model:
        from azure.ai.inference import ChatCompletionsClient
        from azure.ai.inference.models import SystemMessage, UserMessage
        from azure.core.credentials import AzureKeyCredential

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        if isinstance(message, str):
            message = [UserMessage(content=message)]
        if image is not None:
            image_url = image_to_url(image)
            message = [UserMessage(
                    content=[
                        TextContentItem(text=message),
                        ImageContentItem(image_url={"url": "data:image/png;base64," + image_url}),
                    ],
                )]


        response = client.complete(
            messages=message,
            temperature=1.0,
            top_p=1.0,
            max_tokens=4096,
            model=model
        )

    else:
        from openai import OpenAI

        if image is None:
            message = [{"role": "user", "content": message}]
        else:
            image_url = image_to_url(image)
            message = [{"role": "user", "content": [{
                "type": "image_url",
                "image_url": {
                    "url": "data:image/png;base64," + image_url
                }
            }]}]

        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        response = client.chat.completions.create(
            model=model,
            messages=message,
            temperature=1.0,
            top_p=1.0,
            max_tokens=4096
        )

    return response.choices[0].message.content


@register_prompt_handler(api_key_entry="MISTRAL_API_KEY")
def prompt_mistral(message: str, model="mistral-large-2411", image=None):
    """A prompt helper function that sends a message to Mistral.
    If an image is provided, it will use the Pixtral model."""
    import os
    from mistralai import Mistral
    from ._utilities import image_to_url

    if model is None:
        if image is None:
            model = "mistral-large-2411"
        else:
            model = "pixtral-12b-2409"
    if "pixtral" not in model and image is not None:
        model = "pixtral-12b-2409"

    # Retrieve the API key from environment variables
    api_key = os.environ["MISTRAL_API_KEY"]

    # Initialize the Mistral client
    client = Mistral(api_key=api_key)

    # Define the messages for the chat
    if image is None:
        messages = [
            {
                "role": "user",
                "content": message
            }
        ]
    else:
        # Getting the base64 string
        base64_image = image_to_url(image)
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{base64_image}"
                    }
                ]
            }
        ]

    # Get the chat response
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )

    # Print the content of the response
    return chat_response.choices[0].message.content
