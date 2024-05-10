
with open('ege/27-A.txt', 'r') as file:
    data_a = file.read()

with open('ege/27-B.txt', 'r') as file:
    data_b = file.read()

array_a = list(map(int, data_a.split()))  
array_b = list(map(int, data_b.split()))  



for i in range(len(array_a)):
    for j in range(len(array_b)):
        summ = array_a[i] + array_b[j]
        mult = array_a[i] * array_b[j]
        if summ%4 == 0 and mult%6561 == 0:
