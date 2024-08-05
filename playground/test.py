import os

# Define the directory and file path
directory = 'playground/test_folder'
file_path = os.path.join(directory, 'test.md')

# 10 programmer jokes to be added to the Markdown file
jokes = [
    "- Why do programmers prefer dark mode? Because light attracts bugs.",
    "- How many programmers does it take to change a light bulb? None. It's a hardware problem.",
    "- Why do Java developers wear glasses? Because they don't see sharp.",
    "- A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
    "- There are 10 types of people in the world. Those who understand binary and those who don't.",
    "- Why do programmers hate nature? It has too many bugs.",
    "- How do you comfort a JavaScript bug? You console it.",
    "- Why was the developer unhappy at their job? They wanted arrays.",
    "- Why do Python programmers have low self-esteem? Because they're constantly comparing their self to others.",
    "- What is a programmer's favorite hangout place? Foo bar."
]

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Write the jokes to the file
with open(file_path, 'w') as file:
    file.write("# Programmer Jokes\n\n")
    for joke in jokes:
        file.write(f"{joke}\n")

print(f"File created at {file_path}")