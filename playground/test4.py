def faculty(number):
    if number == 0:
        return 1
    else:
        return number * faculty(number - 1)

for i in range(10):
    print("The faculty of", i, "is", faculty(i))
