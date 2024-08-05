import os

# Define the folder and file paths
folder_path = 'playground/test_folder'
file_path = os.path.join(folder_path, 'test.md')

# List of programmer jokes in markdown format
jokes = [
    "### 1. Why do programmers prefer dark mode?\nBecause light attracts bugs.",
    "### 2. How many programmers does it take to change a light bulb?\nNone. It’s a hardware problem.",
    "### 3. Why do programmers hate nature?\nIt has too many bugs.",
    "### 4. How many programmers does it take to screw in a light bulb?\nNone. That's a hardware problem.",
    "### 5. Why do Java developers wear glasses?\nBecause they can't C#.",
    "### 6. What is a programmer's favorite place to hang out?\nThe Foo Bar.",
    "### 7. Why do programmers prefer iOS development?\nBecause Android doesn’t have any class.",
    "### 8. Why do Python programmers have low self-esteem?\nBecause they’re constantly comparing their self to others.",
    "### 9. What do you get when you cross a computer with an elephant?\nLots of memory.",
    "### 10. How do you comfort a JavaScript bug?\nYou console it."
]

def create_folder_and_file():
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    # Write the jokes into the markdown file
    with open(file_path, 'w') as file:
        for joke in jokes:
            file.write(joke + "\n\n")

# Execute the function to create the folder and file
create_folder_and_file()