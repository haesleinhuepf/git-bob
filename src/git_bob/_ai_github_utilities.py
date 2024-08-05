import os

def create_folder_and_file():
    folder_path = "playground/test_folder"
    file_path = os.path.join(folder_path, "test.md")
    jokes = [
        "1. Why do programmers prefer dark mode? Because light attracts bugs.",
        "2. How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "3. Why do Java developers wear glasses? Because they don't see sharp.",
        "4. A programmer walks into a bar and orders 1.000000119 root beers. The bartender says, “I’ll have to charge you extra, that’s a root beer float.” The programmer says, “Well in that case, make it a double.”",
        "5. How do you comfort a JavaScript bug? You console it.",
        "6. Why did the programmer quit his job? Because he didn't get arrays.",
        "7. What is a programmer's favorite hangout place? Foo Bar.",
        "8. How do you know when a programmer is an extrovert? When he looks at your shoes instead of his own.",
        "9. Why do programmers hate nature? It has too many bugs.",
        "10. Why do Python programmers prefer snake_case? Because they don't want to be bitten by the camelCase."
    ]

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, "w") as f:
        f.write("# Programmer Jokes\n\n")
        for joke in jokes:
            f.write(f"{joke}\n\n")

if __name__ == "__main__":
    create_folder_and_file()