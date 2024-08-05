import os

# Create the directory structure
os.makedirs('playground/test_folder', exist_ok=True)

# Define the content of the markdown file with programmer jokes
jokes = """
# Programmer Jokes

1. Why do programmers prefer dark mode? Because light attracts bugs.
2. How many programmers does it take to change a light bulb? None, that's a hardware problem.
3. Why do programmers hate nature? It has too many bugs.
4. Why do Java developers wear glasses? Because they don't see sharp.
5. How do you tell an introverted programmer from an extroverted one? An extroverted programmer looks at your shoes when talking to you.
6. Why do Python programmers have low self esteem? They're constantly comparing their self to others.
7. How do you comfort a JavaScript bug? You console it.
8. Why did the programmer quit his job? Because he didn't get arrays.
9. Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.
10. How do you know a programmer is an extrovert? He looks at your shoes when he's talking to you instead of his own.
"""

# Write jokes to the markdown file
with open('playground/test_folder/test.md', 'w') as file:
    file.write(jokes)

print("test.md file created with 10 programmer jokes in 'playground/test_folder'")