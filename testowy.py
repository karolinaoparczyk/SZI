solutions = [['l', 'p', 'l', 'l', 'p', 'l'], ['l', 'p', 'l'], ['l', 'p', 'l', 'p'], ['l', 'p', 'l', 'p', 'l'], ['l', 'p', 'l', 'l', 'p', 'l', 'l']]
find = 1000
for i in range(len(solutions)):
    if len(solutions[i]) < find:
        find = len(solutions[i])
        index = i

print(solutions[index])
