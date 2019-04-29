import sys
import copy

file_name = input('Which data file do you want to use?')
try:
    file = open(file_name,'r')
    Lines = file.readlines()
    if Lines == []:
        raise ValueError
        sys.exit()
except (IOError, ValueError):
    print('Incorrect Input/Output or Value!')
    sys.exit()

process_Line = []
process_data = []
for line in Lines:
    data = line.split()
    process_data.append(data)
for a in process_data:
    each_Line = []
    for b in a:
        each_Line.append(int(b))
    # print(each_Line)
    process_Line.append(each_Line)
    # process_Line.sort(key=len(process_Line),reverse=True)
    #print('process_Line is ', process_Line)  # 得到每一行的数字，每行各为一个list

# print('lenth=',len(process_Line))
count = 1
l = len(process_Line)
storage = []
sum_outpot = 0
for i in range(l - 1, -1, -1):
    L = []
    path=[]
    #for k in range(0,l):
    k = l - i - 1
    for j in range(0, len(process_Line[i])):
        if i + 1 == l:
            L.append([process_Line[i][j],count,[process_Line[i][j]]])
            path.append([process_Line[i][j]])
            #print('when i+1==l', L)
         #print('L=',L)
         #print('storage=',storage)
        else:
            #print('L=',L)
            #L.append(process_Line[i][j])
            if storage[k - 1][j][0] < storage[k - 1][j + 1][0]:
                sum_output = process_Line[i][j] + storage[k - 1][j + 1][0]  # store larger one
                L.append([sum_output,1,copy.deepcopy(storage[k - 1][j+1][2])])
                L[j][2].append(copy.deepcopy(process_Line[i][j]))
                path.append(copy.deepcopy(process_Line[i][j]))
                path.append(copy.deepcopy(storage[k - 1][j + 1][0]))

            elif storage[k - 1][j][0] == storage[k - 1][j + 1][0]:
                sum_output = process_Line[i][j] + storage[k - 1][j][0]
                L.append([sum_output,count + 1,copy.deepcopy(storage[k - 1][j][2])])
                L[j][2].append(copy.deepcopy(process_Line[i][j]))
                count += 1
                path.append(copy.deepcopy(process_Line[i][j]))
                path.append(storage[k - 1][j][0])

            elif storage[k - 1][j][0] > storage[k - 1][j + 1][0]:
                sum_output = process_Line[i][j] + storage[k - 1][j][0]
                L.append([sum_output,1,copy.deepcopy(storage[k - 1][j][2])])
                L[j][2].append(copy.deepcopy(process_Line[i][j]))
                path.append(copy.deepcopy(process_Line[i][j]))
                path.append(storage[k - 1][j][0])
    storage.append(copy.deepcopy(L))
# sum_outpot =sum(L)
#print('path=',path)
#print('storage=', storage)
#print('path yielding=',storage[-1][-1][2])
print('The largest sum is: ', storage[-1][-1][0])
print('The number of paths yielding this sum is: ', storage[-1][-1][1])
print('The leftmost path yielding this sum is: ', (storage[-1][-1][2])[::-1])
