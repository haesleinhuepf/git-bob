import os

# Define the new directory structure and file path
directory_structure = 'playground/test_folder'
file_path = os.path.join(directory_structure, 'test.md')

# Create the directory if it doesn't exist
os.makedirs(directory_structure, exist_ok=True)

# Define 10 programmer jokes
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
    "Why do programmers hate nature? It has too many bugs.",
    "Why do Java developers wear glasses? Because they don’t C#!",
    "What’s a programmer’s favorite hangout place? Foo Bar.",
    "Why do Python programmers prefer short jokes? Because they're easy to interpret!",
    "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
    "What do computers and air conditioners have in common? They both become useless when you open windows.",
    "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
    "Why was the JavaScript developer crying? Because he couldn't 'callback' his friends."
]

# Create the file and write the jokes
with open(file_path, 'w') as file:
    for joke in jokes:
        file.write(f"{joke}\n")

print(f"File '{file_path}' created with 10 programmer jokes.")