import os

# Define the directory and file paths
directory = "playground/test_folder"
file_path = os.path.join(directory, "test.md")

# Define the programmer jokes
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    "Why do programmers hate nature? It has too many bugs.",
    "Why do Java developers wear glasses? Because they can’t C#.",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "What do you call a programmer from Finland? Nerdic.",
    "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
    "Why did the programmer go broke? Because he used up all his cache.",
    "Why do Python programmers prefer snake_case? Because it’s sssssuperior!",
    "What is a programmer's favorite hangout place? Foo Bar."
]

# Create directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Write jokes to the file in markdown format
with open(file_path, 'w') as file:
    for i, joke in enumerate(jokes, start=1):
        file.write(f"{i}. {joke}\n\n")