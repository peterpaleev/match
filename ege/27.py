
with open('ege/27-A.txt', 'r') as file:
    data_a = file.read()

with open('ege/27-B.txt', 'r') as file:
    data_b = file.read()

array_a = list(map(int, data_a.split()))  
array_b = list(map(int, data_b.split()))  

print(array_a, array_b)