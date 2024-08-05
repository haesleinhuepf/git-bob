import os

def create_jokes_markdown(file_path):
    """
    Create a markdown file containing 10 programmer jokes at the specified file path.
    """
    jokes = [
        "## Programmer Jokes\n",
        "1. Why do programmers prefer dark mode?\n   Because light attracts bugs!\n",
        "2. How many programmers does it take to change a light bulb?\n   None, that's a hardware problem.\n",
        "3. Why do Java developers wear glasses?\n   Because they don't see sharp.\n",
        "4. What is a programmer's favorite hangout place?\n   Foo Bar.\n",
        "5. Why do programmers hate nature?\n   It has too many bugs.\n",
        "6. How do you comfort a JavaScript bug?\n   You console it.\n",
        "7. Why do C# and Java developers keep breaking their keyboards?\n   Because they use a strongly typed language.\n",
        "8. What do you call a programmer from Finland?\n   Nerdic.\n",
        "9. What's the most used language in programming?\n   Profanity.\n",
        "10. Why was the computer cold?\n   It left its Windows open.\n"
    ]

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write jokes to the file
    with open(file_path, 'w') as file:
        file.writelines(jokes)

    print(f"File created at {file_path} with 10 programmer jokes.")

def split_content_and_summary(content):
    """
    Placeholder function to simulate the missing function mentioned in the error log.
    Replace this with actual implementation if needed.
    """
    return content.split('---', 1) if '---' in content else (content, '')

# Example usage (to be removed in production code)
# create_jokes_markdown('playground/test_folder/test.md')