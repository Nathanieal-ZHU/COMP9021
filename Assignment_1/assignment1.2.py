import sys
from math import log2

file_name = input('Which data file do you want to use? ')
try:
    file = open(file_name,'r')
    Lines = file.readlines()
    if Lines == []:
        raise ValueError
        sys.exit()
except (IOError, ValueError):
    print('Incorrect Input/Output or Value!')
    sys.exit()

km = []
kg = []

for line in Lines:
    data = line.split(' ')
    for i in range(len(data)):
        if i % 2 !=0:
            kg.append(int(data[i]))
        else:
            km.append(int(data[i]))
print('km=',km)
print('kg=',kg)
def Average(kg):
    sum = 0
    for a in kg:
        sum +=a
    return sum / len(kg)

average_kg = int(Average(kg))
half = average_kg
min_kg = min(kg)
max_kg = max(kg)
difference = max_kg - min_kg
quantity = []
print('average is',average_kg)
#print('log=',int(log2(difference)))

for i in range(0,int(log2(difference))+1):
    process = kg[:]
    for j in range(0,len(km)-1):
        if process[j] < average_kg:
            process[j+1] = process[j+1] - (average_kg-process[j]) - (km[j+1]-km[j])
        elif process[j] == i:
            pass
        elif process[j] > average_kg:
            if (process[j] - average_kg) - (km[j+1]-km[j]) > 0:
                process[j+1] = process[j+1] + (process[j] - average_kg) - (km[j+1]-km[j])
            else:
                pass
    print('process[-1]=',process[-1])
    if process[-1] == average_kg:
        quantity.append(average_kg)
        #break
        #print('i=',i)
    if process[-1] > average_kg:
        #process = kg
        min_kg = average_kg
        #break
    if process[-1] < average_kg:
        #process = kg
        max_kg = average_kg
        #break
    average_kg = (max_kg + min_kg) // 2
    #print('average=',average_kg)
print(quantity)
print(f'The maximum quantity of fish that each town can have is {quantity[-1]}.')
