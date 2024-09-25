def faculty(number):
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result

for i in range(10):
    print("The faculty of", i, "is", faculty(i))
