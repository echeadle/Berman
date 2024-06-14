# filename: number_output.py

with open('output.txt', 'w') as file:
    for i in range(1, 101):
        file.write(str(i) + '\n')