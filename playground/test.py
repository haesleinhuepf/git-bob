def faculty(number):
    if number == 0:
        return 1
    else:
        return number * faculty(number - 1)

for i in range(10):
    print("The faculty of", i, "is", faculty(i))

# Create a copy of test.py content into test4.py
with open('playground/test4.py', 'w') as f:
    with open(__file__, 'r') as current_file:
        f.write(current_file.read())
