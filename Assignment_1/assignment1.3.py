import sys
from operator import itemgetter

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
        Line = Line.strip()
        #print('Line=', Line)
        Line = Line.split()
        L.append(Line)
        #print('Line=', Line)
except (IOError, ValueError):
    print('Incorrect Input/Output or Value!')
    sys.exit()
print('L=',L)

for i in range(0,len(L)):
    for j in range(0,4):
        L[i][j]=int(L[i][j])
#print('L=',L)

a=[]    #水平方向从左到右排序  sort from left to right

for i in range(0,len(L)):
    x = min(L[i][0],L[i][2])
    y = min(L[i][1],L[i][3])
    X = [x,y]
    x = max(L[i][0],L[i][2])
    y = max(L[i][1],L[i][3])
    Y = [x,y]
    a.append(X+Y)
a.sort()
'''
a = sorted(L,key=itemgetter(0))
'''

b=[]    #垂直方向从下到上排序   sort from down to up

for i in range(0,len(L)):
    x = min(L[i][0],L[i][2])
    y = min(L[i][1],L[i][3])
    X = [y,x]
    x = max(L[i][0],L[i][2])
    y = max(L[i][1],L[i][3])
    Y = [y,x]
    b.append(X+Y)
b.sort()
'''
x=[]
y=[]
for i in range(0,len(L)):
    x = [L[i][0],L[i][1]]
    x = x[::-1]
    y = [L[i][2],L[i][3]]
    y = y[::-1]
    print('x=',x)
    print('y=',y)
    Y = (x+y)
    b.append(Y)
#print('a=',a)
print('b=',b)
'''
def perimeter(a):
  s=0
  for m in a:
    x=m[0]
    y=m[1]
    #print('x=',x)
    #print('y=',y)
    while y<m[3]:
      for n in a:
        if n[1]<=y<n[3] and n[0]<x<n[2]:  #select overlap points
          y=y+1
          break
        if n==a[-1]:
          y=y+1
          s=s+1
  #print('s=',s)
  return(s)

C = 2*perimeter(a) + 2*perimeter(b)
#print('verti_C=',perimeter(b))
#print('horizon_C=',perimeter(a))
print('The perimeter is:',C)


####交作业时，求a、b使用的是引号中的版本