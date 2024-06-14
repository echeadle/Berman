# filename: numbers.py

with open('output.txt', 'w') as file:
    for i in range(1, 201):
        file.write(str(i) + '\n')