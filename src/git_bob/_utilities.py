import os

def create_folders_and_file():
    """
    Creates the 'playground/test_folder/test.md' file with 10 programmer jokes.
    The function ensures that the necessary directory structure exists.
    """
    directory_path = 'playground/test_folder'
    file_path = os.path.join(directory_path, 'test.md')
    
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    
    # Programmer jokes to be written in the markdown file
    jokes = [
        "1. Why do programmers prefer dark mode? Because light attracts bugs.",
        "2. How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "3. Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
        "4. What's a programmer's favorite hangout place? Foo Bar.",
        "5. Why do Java developers wear glasses? Because they don’t C#.",
        "6. How do you comfort a JavaScript bug? You console it.",
        "7. Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "8. What do you call a programmer from Finland? Nerdic.",
        "9. Why do programmers hate nature? It has too many bugs.",
        "10. Why did the programmer quit his job? Because he didn’t get arrays."
    ]
    
    # Write the jokes to the file in markdown format
    with open(file_path, 'w') as f:
        for joke in jokes:
            f.write(f"{joke}\n\n")  # Markdown format with new lines between jokes

if __name__ == "__main__":
    create_folders_and_file()