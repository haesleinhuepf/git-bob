import os

def create_folder_and_file():
    # Define the directory and file paths
    directory = os.path.join('playground', 'test_folder')
    file_path = os.path.join(directory, 'test.md')

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # List of 10 programmer jokes in markdown format
    jokes = [
        "1. Why do programmers prefer dark mode? **Because the light attracts bugs!**",
        "2. How many programmers does it take to change a light bulb? **None, that's a hardware problem!**",
        "3. Why do Java developers wear glasses? **Because they can't C#!**",
        "4. What's a programmer's favorite hangout place? **Foo Bar!**",
        "5. Why do Python programmers prefer to eat Python eggs? **Because it has a better import!**",
        "6. Debugging: Removing the needles from the haystack.",
        "7. Why was the JavaScript developer sad? **Because he didn't know how to 'null' his feelings!**",
        "8. Why do programmers prefer using the terminal? **Because it’s CLI-side!**",
        "9. How does a computer get drunk? **It takes screenshots!**",
        "10. Why do programmers hate nature? **It has too many bugs!**"
    ]

    # Write the jokes to the file
    with open(file_path, 'w') as file:
        file.write('\n'.join(jokes))

if __name__ == "__main__":
    create_folder_and_file()