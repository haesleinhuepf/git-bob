import os

def create_folders_and_file():
    # Define the path to the new folder and file
    target_folder = 'playground/test_folder'
    target_file = os.path.join(target_folder, 'test.md')

    # Create the new folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # Define the 10 programmer jokes in markdown format
    jokes = [
        "1. Why do programmers prefer dark mode? Because light attracts bugs.",
        "2. How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "3. Why do Java developers wear glasses? Because they can't C#.",
        "4. A SQL statement walks into a bar and sees two tables. It approaches, and asks 'May I join you?'",
        "5. How do you comfort a JavaScript bug? You console it.",
        "6. Why don't programmers like nature? It has too many bugs.",
        "7. What's a programmer's favorite place to hangout? The Foo Bar.",
        "8. Why do programmers hate nature? It has too many bugs.",
        "9. How do you know you are talking to a UNIX admin? They keep saying 'sudo make me a sandwich'.",
        "10. Why was the JavaScript developer sad? Because he didn't know how to 'null' his emotions."
    ]

    # Join the jokes into a single string separated by newlines
    jokes_content = "\n\n".join(jokes)

    # Write the jokes to the target file
    with open(target_file, 'w') as f:
        f.write(jokes_content)

# If this module is executed, run the function
if __name__ == "__main__":
    create_folders_and_file()