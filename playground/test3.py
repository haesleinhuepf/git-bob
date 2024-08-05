import os

# Define the path and file name
folder_path = 'playground/test_folder'
file_name = 'test.md'
file_path = os.path.join(folder_path, file_name)

# Ensure the directory exists
os.makedirs(folder_path, exist_ok=True)

# Jokes to be written in the test.md file
jokes = [
    '### Programmer Joke 1\nWhy do programmers prefer dark mode? Because light attracts bugs.\n',
    '### Programmer Joke 2\nWhy do Java developers wear glasses? Because they can’t C#.\n',
    '### Programmer Joke 3\nHow many programmers does it take to change a light bulb? None. It’s a hardware problem.\n',
    '### Programmer Joke 4\nWhy do programmers hate nature? It has too many bugs.\n',
    '### Programmer Joke 5\nWhat do you call a programmer from Finland? Nerdic.\n',
    '### Programmer Joke 6\nWhy did the programmer quit his job? Because he didn’t get arrays.\n',
    '### Programmer Joke 7\nWhat is a programmer’s favorite hangout place? Foo Bar.\n',
    '### Programmer Joke 8\nWhy was the JavaScript developer sad? Because he didn’t know how to `null` his feelings.\n',
    '### Programmer Joke 9\nWhy do Python programmers prefer snake_case? Because it’s easier to type_than_CamelCase.\n',
    '### Programmer Joke 10\nWhat’s a programmer’s favorite snack? Microchips!\n'
]

# Write the jokes to the file
with open(file_path, 'w') as f:
    for joke in jokes:
        f.write(joke + '\n')

print(f"{file_name} created with 10 programmer jokes.")