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
max_tokens=4096,
messages=message,
model=model,
)

# extract answer
return message.content[0].text


def prompt_chatgpt(message: str, model="gpt-4o-2024-08-06"):
"""A prompt helper function that sends a message to openAI
and returns only the text response.
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


def prompt_gemini(request, model="gemini-1.5-flash-001"):
"""Send a prompt to Google Gemini and return the response"""
from google import generativeai as genai
import os
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

client = genai.GenerativeModel(model)
result = client.generate_content(request)
return result.text
