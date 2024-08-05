import os

def create_folder_and_file():
    # Define the target path for the new file
    target_dir = "playground/test_folder"
    target_file = os.path.join(target_dir, "test.md")

    # Create the directories if they do not exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # List of 10 programmer jokes in markdown format
    jokes = """
# Programmer Jokes

1. **Why do programmers prefer dark mode?**  
   Because light attracts bugs.

2. **How many programmers does it take to change a light bulb?**  
   None. It's a hardware problem.

3. **Why do programmers hate nature?**  
   It has too many bugs.

4. **Why do Java developers wear glasses?**  
   Because they don't C#.

5. **Why was the function so good at his job?**  
   Because he had a lot of 'arguments'.

6. **Why did the programmer quit his job?**  
   Because he didn't get arrays.

7. **What do you call a programmer from Finland?**  
   Nerdic.

8. **Why do Python programmers have low self-esteem?**  
   They're constantly comparing their self to other.

9. **How do you find an attractive computer programmer?**  
   You check their 'cache'.

10. **Why did the developer go broke?**  
    Because he used up all his cache.

"""

    # Write the jokes to the file
    with open(target_file, 'w') as file:
        file.write(jokes)

if __name__ == "__main__":
    create_folder_and_file()