import os

def create_file_with_jokes():
    # Define the directory and file path
    directory = 'playground/test_folder'
    file_path = os.path.join(directory, 'test.md')

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # List of programmer jokes
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why do Java developers wear glasses? Because they can't C#!",
        "How many programmers does it take to change a light bulb? None, that's a hardware issue.",
        "Why do Python developers prefer snake_case? Because they can't handle CamelCase.",
        "Why was the developer unhappy at their job? They wanted arrays.",
        "Why do programmers hate nature? It has too many bugs.",
        "Why do programmers prefer dogs? Cats turn their code into bytecode.",
        "How do you comfort a JavaScript bug? You console it!",
        "Why was the JavaScript developer sad? Because they didn't know how to 'null' their feelings.",
        "What's a programmer's favorite hangout place? Foo Bar."
    ]

    # Write the jokes to the file in markdown format
    with open(file_path, 'w') as file:
        for joke in jokes:
            file.write(f"- {joke}\n")

# Usage
if __name__ == "__main__":
    create_file_with_jokes()