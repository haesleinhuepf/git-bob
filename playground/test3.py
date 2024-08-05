import os

# Define the directory and file path
directory = "playground/test_folder"
file_path = os.path.join(directory, "test.md")

# Define the jokes to be added to the markdown file
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    "Why do Java developers wear glasses? Because they can't C#.",
    "What is a programmer's favorite hangout place? Foo Bar.",
    "Why do Python programmers prefer to eat snake meat? Because it's Pythonic!",
    "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "What do you call a programmer from Finland? Nerdic.",
    "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
    "Why was the developer bored at the party? Because he was in a nested loop."
]

# Ensure the directory exists
os.makedirs(directory, exist_ok=True)

# Write the jokes to the file
with open(file_path, 'w') as file:
    for joke in jokes:
        file.write(f"- {joke}\n")