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

    Example models: claude-3-5-sonnet-20240620 or claude-3-opus-20240229
    """
    from anthropic import Anthropic

    # convert message in the right format if necessary
    if isinstance(message, str):
        message = [{"role": "user", "content": message}]

    # setup connection to the LLM
    client = Anthropic()

    message = client.messages.create(
        max_tokens=8192 if model == "claude-3-5-20240620" else 4096,
        messages=message,
        model=model,
        extra_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"} if model == "claude-3-5-20240620" else None,
    )

    # extract answer
    return message.content[0].text


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
                    "image_url": {"url": image_url}
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


def prompt_gemini(request, model="gemini-1.5-flash-001"):
    """Send a prompt to Google Gemini and return the response"""
    from google import generativeai as genai
    import os
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    client = genai.GenerativeModel(model)
    result = client.generate_content(request)
    return result.text


def prompt_azure(message: str, model="gpt-4o", image=None):
    """A prompt helper function that sends a message to Azure's OpenAI Service
    and returns only the text response.
    """
    import os
    from ._utilities import image_to_url

    token = os.environ["GH_MODELS_API_KEY"]
    endpoint = "https://models.inference.ai.azure.com"
    model = model.replace("github_models:", "")

    if "gpt" not in model:
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
                        ImageContentItem(image_url={"url": image_url}),
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
                    "url": image_url
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
