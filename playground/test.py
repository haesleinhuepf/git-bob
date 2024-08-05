import os

# Define the directory and filename
directory = 'playground/test_folder'
filename = 'test.md'

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# List of programmer jokes
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "How many programmers does it take to change a light bulb? None, that's a hardware issue.",
    "Why do programmers hate nature? It has too many bugs.",
    "What do you call a programmer from Finland? Nerdic.",
    "Why do Java developers wear glasses? Because they don't C#.",
    "How do you comfort a JavaScript bug? You console it.",
    "Why was the developer unhappy at their job? They wanted arrays.",
    "What's a programmer’s favorite hangout place? Foo Bar.",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "Why do programmers prefer using the dark mode? Because light attracts bugs."
]

# Create or overwrite the markdown file with jokes
with open(os.path.join(directory, filename), 'w') as file:
    for joke in jokes:
        file.write(f"- {joke}\n")

print(f"{filename} has been created with programmer jokes.")