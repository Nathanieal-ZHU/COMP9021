import sys
import re
#from collections import deque

file_name = input('Which data file do you want to use?')
try:
    file = open(file_name, 'r')
    L=[]
    while True:
        Line = file.readline()
        #print('Line=',Line)
        if Line == '':
            break
        if Line == []:
            raise ValueError
            sys.exit()
        Line = re.sub('\s','',Line)
        print('Line=',Line)
        data = re.split(r'[R|(|,|)|\n]', Line)
        print('data=',data)
        data_append = [int(data[2]),int(data[3])]
        L.append(data_append)
except (IOError, ValueError):
    print('Incorrect Input/Output or Value!')
    sys.exit()

#print('Line=',Line)
#print(data)

print('L=',L)
process=[]

for i in L:
    for j in L:
        if i[1]==j[0] and [i[0],j[1]] not in process:  #合并路线
            process.append([i[0],j[1]])
process_1=process
print('process_1=',process_1)

for i in process:
    for j in L:
        if i == j :
            L.remove(j)
        else:
            if i[1] == j[0] and [i[0], j[1]] not in process:
                process.append([i[0], j[1]])

print('process=',process)


print('The nonredundant facts are: ')
for i in L:
    if i not in process:    #剔除重复的
        print('R({},{})'.format(i[0], i[1]))