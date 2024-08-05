import os

# Define the folder and file paths
folder_path = 'playground/test_folder'
file_path = os.path.join(folder_path, 'test.md')

# Define the content with 10 programmer jokes in markdown format
content = """# Programmer Jokes

1. Why do programmers prefer dark mode? Because light attracts bugs.
2. How many programmers does it take to change a light bulb? None, that's a hardware problem.
3. Why do programmers hate nature? It has too many bugs.
4. Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25.
5. I told my computer I needed a break, and now it won't stop sending me KitKats.
6. What's a programmer's favorite hangout place? Foo Bar.
7. Why do programmers always get Christmas and Halloween mixed up? Because 31 OCT = 25 DEC.
8. How many programmers does it take to screw in a lightbulb? None. It's a hardware issue.
9. Debugging: Removing the needles from the haystack.
10. Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.
"""

# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)

# Write the content to the file
with open(file_path, 'w') as file:
    file.write(content)

print("File created successfully!")