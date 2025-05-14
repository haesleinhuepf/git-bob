"""
This module provides helper functions to interact with different language models.
"""

def prompt_anthropic(message: str, model="claude-3-5-sonnet-20241022", image=None):
    """
    A prompt helper function that sends a message to anthropic
    and returns only the text response.

    Example models: claude-3-5-sonnet-20240620 or claude-3-opus-20240229
    """
    from anthropic import Anthropic
    from ._utilities import image_to_url
    import base64
    import numpy as np

    model = model.replace("anthropic:", "")
    model = model.replace("claude:", "")

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


def prompt_openai(message: str, model="gpt-4o-2024-08-06", image=None, max_accumulated_responses=10, max_response_tokens=16384, base_url=None, api_key=None):
    """A prompt helper function that sends a message to openAI
    and returns only the text response.
    """
    # convert message in the right format if necessary
    from ._utilities import image_to_url
    import openai
    import warnings
    from ._utilities import append_result

    model = model.replace("openai:", "")

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

def prompt_kisski(message: str, model=None, image=None, max_accumulated_responses=10, max_response_tokens=16384, base_url=None, api_key=None):
    import os
    if base_url is None:
        base_url = "https://chat-ai.academiccloud.de/v1"
    if api_key is None:
        api_key = os.environ.get("KISSKI_API_KEY")
    model = model.replace("kisski:", "")
    return prompt_openai(message, model=model, image=image, max_accumulated_responses=max_accumulated_responses, max_response_tokens=max_response_tokens, base_url=base_url, api_key=api_key)


def prompt_blablador(message: str, model=None, image=None, max_accumulated_responses=10, max_response_tokens=16384, base_url=None, api_key=None):
    import os
    if base_url is None:
        base_url = "https://helmholtz-blablador.fz-juelich.de:8000/v1"
    if api_key is None:
        api_key = os.environ.get("BLABLADOR_API_KEY")
    model = model.replace("blablador:", "")
    return prompt_openai(message, model=model, image=image, max_accumulated_responses=max_accumulated_responses, max_response_tokens=max_response_tokens, base_url=base_url, api_key=api_key)


def prompt_deepseek(message: str, model="deepseek-chat", image=None, max_accumulated_responses=10, max_response_tokens=8192, base_url=None, api_key=None):
    import os
    if base_url is None:
        base_url = "https://api.deepseek.com"
    if api_key is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
    model = model.replace("deepseek:", "")
    return prompt_openai(message, model=model, image=image, max_accumulated_responses=max_accumulated_responses, max_response_tokens=max_response_tokens, base_url=base_url, api_key=api_key)


def prompt_googleai(request, model="gemini-1.5-pro-002", image=None):
    """Send a prompt to Google Gemini and return the response"""
    from google import generativeai as genai
    import os

    model = model.replace("googleai:", "")

    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    client = genai.GenerativeModel(model)
    
    if image is not None:
        response = client.generate_content([image, request])
    else:
        response = client.generate_content(request)
        
    return response.text


def prompt_azure(message: str, model="gpt-4o", image=None):
    """A prompt helper function that sends a message to Azure's OpenAI Service
    and returns only the text response.
    """
    import os
    from ._utilities import image_to_url

    token = os.environ["GH_MODELS_API_KEY"]
    endpoint = "https://models.inference.ai.azure.com"
    model = model.replace("github_models:", "")
    model = model.replace("azure:", "")

    if "gpt" not in model and "o1" not in model:
        from azure.ai.inference import ChatCompletionsClient
        from azure.ai.inference.models import SystemMessage, UserMessage, TextContentItem, ImageContentItem
        from azure.core.credentials import AzureKeyCredential

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )


        if image is not None:
            image_url = image_to_url(image)
            message = [UserMessage(
                    content=[
                        TextContentItem(text=message),
                        ImageContentItem(image_url={"url": "data:image/png;base64," + image_url}),
                    ],
                )]
        else:
            if isinstance(message, str):
                message = [UserMessage(content=message)]


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


def prompt_mistral(message: str, model="mistral-large-2411", image=None):
    """A prompt helper function that sends a message to Mistral.
    If an image is provided, it will use the Pixtral model."""
    import os
    from mistralai import Mistral
    from ._utilities import image_to_url

    model = model.replace("mistral:", "")
    model = model.replace("pixtral:", "")

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


def text_to_speech_openai(text:str, filename:str, model:str="tts-1", voice:str="alloy"):
    from openai import OpenAI

    client = OpenAI()
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )

    # Save the audio file
    response.stream_to_file(filename)


def prompt_e_infra_cz(message: str, model="llama3.3:latest", image=None):
    """A prompt helper function that sends a message to e-infra_cz
    and returns only the text response.
    """
    import os
    from ._utilities import image_to_url

    base_url = "https://chat.ai.e-infra.cz/api/"
    api_key = os.environ.get("E_INFRA_CZ_API_KEY")
    model = model.replace("e-infra_cz:", "")

    return prompt_openai(message, model=model, image=image, base_url=base_url, api_key=api_key)
