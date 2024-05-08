seq_1 = []
seq_2 = []

found = [0,0]

for i in len(seq_1):
    for j in len(seq_2):
        if j > i:
            if seq_1[i] > seq_2[j]:
                suspect = seq_1[i] + seq_2[j]
                if suspect%113==0:
                    if suspect > found:
                        found = suspect

print(found)