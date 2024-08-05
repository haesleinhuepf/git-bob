import os

# Define the directory and file to be created
directory = "playground/test_folder"
file_path = os.path.join(directory, "test.md")

# Ensure the directory exists
os.makedirs(directory, exist_ok=True)

# List of 10 programmer jokes
jokes = [
    "1. Why do programmers prefer dark mode? Because light attracts bugs.",
    "2. Why do Java developers wear glasses? Because they can’t C#.",
    "3. How many programmers does it take to change a light bulb? None. It's a hardware problem.",
    "4. Why do programmers hate nature? It has too many bugs.",
    "5. How do you comfort a JavaScript bug? You console it.",
    "6. Why do Python programmers prefer snake_case? Because it's not Monty Case.",
    "7. What is a programmer’s favorite hangout place? Foo Bar.",
    "8. Why do programmers confuse Christmas and Halloween? Because Oct 31 == Dec 25.",
    "9. How do you know if a developer is an extrovert? They look at your shoes when they talk to you.",
    "10. What do you call a programmer from Finland? Nerdic."
]

# Write the jokes to the markdown file
with open(file_path, 'w') as file:
    for joke in jokes:
        file.write(f"{joke}\n\n")

print(f"File {file_path} created with 10 programmer jokes.")