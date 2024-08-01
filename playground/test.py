# This function calculates the factorial of a given number

def faculty(number):
    if number == 0:
        return 1
    else:
        return number * faculty(number - 1)

# Print the factorial of numbers from 0 to 9
for i in range(10):
    print("The faculty of", i, "is", faculty(i))