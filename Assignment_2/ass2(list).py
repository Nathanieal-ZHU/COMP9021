import sys
import os
import copy

class FriezeError(Exception):
    def __init__(self,message):
        self.message = message
class Frieze:
    def __init__(self,name):
        self.name = name
        self.filedata=[]
        self.file = open(name)
        self.filedata = self.file.readlines()
        self.filedata = [x.strip('\n') for x in self.filedata]
        self.rows = []
        for L in self.filedata:
            self.rows.append([int(v) for v in L.split()])
        self.flag = True
        self.data = []
        self.firstline = (4,12)
        self.finalline = (4,5,6,7)
        for i in range(len(self.filedata)):
            if self.rows[i] != []:
                self.data.append(self.rows[i])
        length = len(self.data[0])
        for i in range(len(self.data)):
            if len(self.data[i]) != length:
                self.flag = False
                break
            for j in range(len(self.data[i])):
                if self.data[i][j] not in range(0,15):
                    self.flag = False
                    break
            if self.flag == False:
                break
        if len(self.data) not in range(3,17):
            self.flag = False
        if len(self.data[0]) not in range(5,51):
            self.flag = False
        if self.flag == False:
            raise FriezeError('Incorrect input.')
        self.flag_frieze = True
        if self.data[0][len(self.data[0])-1] != 0:
            self.flag_frieze = False
        for i in range(1,len(self.data)):
            if self.data[i][len(self.data[0])-1] >1:
                self.flag_frieze = False
                break
        for i in range(0,len(self.data[0])-1):
            if self.data[0][i] not in self.firstline:
                self.flag_frieze = False
                break
            if self.data[len(self.data)-1][i] not in self.finalline:
                self.flag_frieze = False
                break
        self.pflag = True
        self.period=0
        for i in range(1,round(len(self.data[0])/2)+1):
            if self.data[0][0:i] == self.data[0][i:i+i]:
                self.pflag = True
                for j in range(1,len(self.data)):
                    if self.data[j][0:i] != self.data[j][i:i+i]:
                        self.pflag = False
                        break
                if self.pflag == True:
                    self.period=i
                    break
        if self.period == 0:
            self.flag_frieze = False
        self.north = copy.deepcopy(self.data)
        self.north_east = copy.deepcopy(self.data)
        self.east = copy.deepcopy(self.data)
        self.south_east = copy.deepcopy(self.data)
        self.data_2 = copy.deepcopy(self.data)
        for i in range(0,len(self.data)):
            for j in range(0, len(self.data[i])):
                if (self.data_2[i][j] - 8) >= 0:
                    self.south_east[i][j] = 1
                    self.data_2[i][j] = self.data_2[i][j] - 8
                else:
                    self.south_east[i][j] =0
        for i in range(0,len(self.data)):
            for j in range(0, len(self.data[i])):
                if (self.data_2[i][j] - 4) >= 0:
                    self.east[i][j] = 1
                    self.data_2[i][j] = self.data_2[i][j] - 4
                else:
                    self.east[i][j] =0
        for i in range(0,len(self.data)):
            for j in range(0, len(self.data[i])):
                if (self.data_2[i][j] - 2) >= 0:
                    self.north_east[i][j] = 1
                    self.data_2[i][j] = self.data_2[i][j] - 2
                else:
                    self.north_east[i][j] =0
        for i in range(0,len(self.data)):
            for j in range(0, len(self.data[i])):
                if (self.data_2[i][j] - 1) == 0:
                    self.north[i][j] = 1
                else:
                    self.north[i][j] =0
        for i in range(0,len(self.south_east)-1):
            for j in range(0,len(self.north_east[i])):
                if self.south_east[i][j] ==1:
                    if self.north_east[i+1][j] ==1:
                        self.flag_frieze =False
                        break
            if self.flag_frieze == False:
                break

        if self.flag_frieze == False:
            raise FriezeError('Input does not represent a frieze.')
    
    
    def analyse(self):
        vflag=self.vertical()
        hflag=self.horizontal()
        ghflag=self.glided_horizontal()
        rflag = self.rotation()
        if vflag == True and hflag == False and ghflag == False:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and vertical reflection only.\n')
        if vflag == False and hflag == True:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and horizontal reflection only.\n')
        if vflag == True and hflag == True:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        horizontal and vertical reflections, and rotation only.\n')
        if vflag == False and ghflag == True:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and glided horizontal reflection only.\n')
        if vflag == True and ghflag == True:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        glided horizontal and vertical reflections, and rotation only.\n')
        if vflag == False and hflag == False and rflag == False and ghflag == False:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation only.\n')
        if vflag == False and hflag == False and ghflag == False and rflag == True:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and rotation only.\n')
    
    
    
    def vertical(self):
        self.apflag = False
        if self.period % 2 == 0:
            self.length = int(self.period/2)
            self.nflag = False
            self.rflag = False
            for i in range(self.period):
                for j in range(len(self.north)):
                    self.nflag = True
                    s = self.north[j][i:i+self.length]
                    s.reverse()
                    if self.north[j][i+self.length:i+self.length+self.length] != s:
                        self.nflag = False
                        break
                if self.nflag == True:
                    self.eflag = False
                    for j in range(len(self.east)):
                        self.eflag = True
                        s = self.east[j][i:i+self.length]
                        s.reverse()
                        if self.east[j][i+self.length-1:i+self.length+self.length-1] != s:
                            self.eflag = False
                            break
                    if self.eflag == True:
                        self.neflag = False
                        for j in range(1,len(self.north_east)):
                            self.neflag = True
                            s = self.north_east[j][i:i+self.length]
                            s.reverse()
                            if self.south_east[j-1][i+self.length-1:i+self.length+self.length-1] != s:
                                self.neflag = False
                                break
                        if self.neflag == True:
                            self.seflag = False
                            for j in range(len(self.south_east)-1):
                                self.seflag = True
                                s = self.south_east[j][i:i+self.length]
                                s.reverse()
                                if self.north_east[j+1][i+self.length-1:i+self.length+self.length-1] != s:
                                    self.seflag = False
                                    break
                            if self.seflag == True:
                                return True
            if self.rflag == False:
                self.apflag = True
                self.period = self.period + 1
        if self.period % 2 == 1:
            self.length = int(self.period/2)
            self.nflag = False
            for i in range(self.period):
                for j in range(len(self.north)):
                    self.nflag = True
                    s = self.north[j][i:i+self.length]
                    s.reverse()
                    if self.north[j][i+self.length+1:i+self.length+self.length+1] != s:
                        self.nflag = False
                        break
                if self.nflag == True:
                    self.eflag = False
                    for j in range(len(self.east)):
                        self.eflag = True
                        s = self.east[j][i:i+self.length]
                        s.reverse()
                        if self.east[j][i+self.length:i+self.length+self.length] != s:
                            self.eflag = False
                            break
                    if self.eflag == True:
                        self.neflag = False
                        for j in range(1,len(self.north_east)):
                            self.neflag = True
                            s = self.north_east[j][i:i+self.length]
                            s.reverse()
                            if self.south_east[j-1][i+self.length:i+self.length+self.length] != s:
                                self.neflag = False
                                break
                        if self.neflag == True:
                            self.seflag = False
                            for j in range(len(self.south_east)-1):
                                self.seflag = True
                                s = self.south_east[j][i:i+self.length]
                                s.reverse()
                                if self.north_east[j+1][i+self.length:i+self.length+self.length] != s:
                                    self.seflag = False
                                    break
                            if self.seflag == True:
                                self.period = self.period - 1
                                return True
            if self.apflag == True:
                self.period =self.period - 1
        return False
    
    def horizontal(self):
        self.height = len(self.data)
        self.new_north = [[row[i] for row in self.north] for i in range(len(self.north[0]))]
        self.new_north_east = [[row[i] for row in self.north_east] for i in range(len(self.north_east[0]))]
        self.new_east = [[row[i] for row in self.east] for i in range(len(self.east[0]))]
        self.new_south_east = [[row[i] for row in self.south_east] for i in range(len(self.south_east[0]))]
        if self.height % 2 == 0:
            self.length = int(self.height / 2)
            self.nflag = False
            for i in range(len(self.new_north)):
                self.nflag = True
                s = self.new_north[i][1:self.length]
                s.reverse()
                if s != self.new_north[i][self.length+1:len(self.new_north[i])]:
                    self.nflag = False
                    break
            if self.nflag == True:
                self.neflag = False
                for i in range(len(self.new_north_east)):
                    self.neflag = True
                    s = self.new_north_east[i][0:self.length]
                    s.reverse()
                    if s != self.new_south_east[i][self.length:len(self.new_north_east[i])]:
                        self.neflag = False
                        break
                if self.neflag == True:
                    self.eflag = False
                    for i in range(len(self.new_east)):
                        self.eflag = True
                        s = self.new_east[i][0:self.length]
                        s.reverse()
                        if s != self.new_east[i][self.length:len(self.new_east[i])]:
                            self.eflag = False
                            break
                    if self.eflag == True:
                        self.seflag = False
                        for i in range(len(self.new_south_east)):
                            self.seflag = True
                            s = self.new_south_east[i][0:self.length]
                            s.reverse()
                            if s != self.new_north_east[i][self.length:len(self.new_south_east[i])]:
                                self.seflag = False
                                break
                        if self.seflag == True:
                            return True
        if self.height % 2 == 1:
            self.length = int(self.height / 2)
            self.nflag = False
            for i in range(len(self.new_north)):
                self.nflag = True
                s= self.new_north[i][1: self.length+1]
                s.reverse()
                if s != self.new_north[i][self.length+1:]:
                    self.nflag = False
                    break
            if self.nflag == True:
                self.neflag = False
                for i in range(len(self.new_north_east)):
                    self.neflag = True
                    s = self.new_north_east[i][0:self.length]
                    s.reverse()
                    if s != self.new_south_east[i][self.length+1:]:
                        self.neflag = False
                        break
                    if self.new_north_east[i][self.length] == 1:
                        self.neflag = False
                        break
                if self.neflag == True:
                    self.efalg = False
                    for i in range(len(self.new_east)):
                        self.eflag = True
                        s = self.new_east[i][0:self.length]
                        s.reverse()
                        if s != self.new_east[i][self.length+1:]:
                            self.eflag = False
                            break
                    if self.eflag == True:
                        self.seflag = False
                        for i in range(len(self.new_south_east)):
                            self.seflag = True
                            s = self.new_south_east[i][0:self.length]
                            s.reverse()
                            if s != self.new_north_east[i][self.length+1:]:
                                self.seflag = False
                                break
                            if self.new_south_east[i][self.length] == 1:
                                self.seflag = False
                        if self.seflag == True:
                            return True
        return False
    
    def glided_horizontal(self):
        self.height = len(self.data)
        self.new_north = [[row[i] for row in self.north] for i in range(len(self.north[0]))]
        self.new_north_east = [[row[i] for row in self.north_east] for i in range(len(self.north_east[0]))]
        self.new_east = [[row[i] for row in self.east] for i in range(len(self.east[0]))]
        self.new_south_east = [[row[i] for row in self.south_east] for i in range(len(self.south_east[0]))]
        if self.period % 2 == 1:
            return False
        if self.period % 2 == 0:
            self.pd = int(self.period/2)
            if self.height % 2 == 0:
                self.length = int(self.height/2)
                self.nflag = False
                for i in range(self.pd):
                    for j in range(len(self.new_north)-self.period):
                        self.nflag = True
                        s = self.new_north[j][1:self.length]
                        s.reverse()
                        if s != self.new_north[j+i+self.pd][self.length+1:]:
                            self.nflag = False
                            break
                    if self.nflag == True:
                        self.nefalg = False
                        for j in range(len(self.new_north_east)-self.period):
                            self.neflag = True
                            s = self.new_north_east[j][0:self.length]
                            s.reverse()
                            if s != self.new_south_east[j+i+self.pd][self.length:]:
                                self.neflag = False
                                break
                        if self.neflag == True:
                            self.eflag = False
                            for j in range(len(self.new_east)-self.period):
                                self.eflag = True
                                s = self.new_east[j][0:self.length]
                                s.reverse()
                                if s != self.new_east[i+j+self.pd][self.length:]:
                                    self.eflag = False
                                    break
                            if self.eflag == True:
                                self.seflag = False
                                for j in range(len(self.new_south_east)-self.period):
                                    self.seflag = True
                                    s = self.new_south_east[j][0:self.length]
                                    s.reverse()
                                    if s !=self.new_south_east[i+j+self.pd][self.length:]:
                                        self.seflag = False
                                        break
                                if self.seflag == True:
                                    return True
            if self.height % 2 == 1:
                self.length = int(self.height / 2)
                self.nflag = False
                for j in range(self.pd):
                    for i in range(len(self.new_north)-self.period):
                        self.nflag = True
                        s= self.new_north[i][1: self.length+1]
                        s.reverse()
                        if s != self.new_north[i+j+self.pd][self.length+1:]:
                            self.nflag = False
                            break
                    if self.nflag == True:
                        self.neflag = False
                        for i in range(len(self.new_north_east)-self.period):
                            self.neflag = True
                            s = self.new_north_east[i][0:self.length]
                            s.reverse()
                            if s != self.new_south_east[i+j+self.pd][self.length+1:]:
                                self.neflag = False
                                break
                            if self.new_north_east[i][self.length] == 1:
                                self.neflag = False
                                break
                        if self.neflag == True:
                            self.efalg = False
                            for i in range(len(self.new_east)-self.period):
                                self.eflag = True
                                s = self.new_east[i][0:self.length]
                                s.reverse()
                                if s != self.new_east[i+j+self.pd][self.length+1:]:
                                    self.eflag = False
                                    break
                            if self.eflag == True:
                                self.seflag = False
                                for i in range(len(self.new_south_east)-self.period):
                                    self.seflag = True
                                    s = self.new_south_east[i][0:self.length]
                                    s.reverse()
                                    if s != self.new_north_east[i+j+self.pd][self.length+1:]:
                                        self.seflag = False
                                        break
                                    if self.new_south_east[i][self.length] == 1:
                                        self.seflag = False
                                if self.seflag == True:
                                    return True
        return False
    
    
    def rotation(self):
        self.height = len(self.data)
        for i in range(self.period):
            for j in range(self.height):
                for m in range(self.period):
                    self.rflag = True
                    if j !=0 :
                        if self.north[j][i+m] != self.north[self.height-j][i+self.period-m]:
                            self.rflag = False
                            break  
                        if self.north_east[j][i+m] != self.north_east[self.height-j][i+self.period-1-m]:
                            self.rflag = False
                            break
                    if self.east[j][i+m] != self.east[self.height-1-j][i+self.period-1-m]:
                        self.rflag = False
                        break
                    if self.south_east[j][i+m] != self.south_east[self.height-2-j][i+self.period-1-m]:
                        self.rflag = False
                        break
                if self.rflag == False:
                    break
            if self.rflag == True:
                    return True
        return False
            
  
    def display(self):
        filename = self.name.split('.')[0] + '.tex'
        file = open(filename,'w')
        file.write('\\documentclass[10pt]{article}\n')
        file.write('\\usepackage{tikz}\n')
        file.write('\\usepackage[margin=0cm]{geometry}\n')
        file.write('\\pagestyle{empty}\n')
        file.write('\n')
        file.write('\\begin{document}\n')
        file.write('\n')
        file.write('\\vspace*{\\fill}\n')
        file.write('\\begin{center}\n')
        file.write('\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]\n')
        file.write('% North to South lines\n')
        n = 0
        s = 0
        list_node = set()
        for i in range(len(self.north[0])):
            for j in range(len(self.north)):
                if self.north[j][i] == 1 and (j,i) not in list_node:
                    list_node.add((j,i))
                    file.write('    \\draw ('+str(i)+','+str(j-1)+')')
                    m = j
                    while m < len(self.north)-1:
                        m = m + 1
                        if self.north[m][i] == 1:
                            list_node.add((m,i))
                        else:
                            break
                    if self.north[m][i] == 1:
                        m= m+1
                    file.write(' -- ('+str(i)+','+str(m-1)+');\n')
        list_node = set()
        file.write('% North-West to South-East lines\n')
        list_node = set()
        for i in range(len(self.south_east)):
            for j in range(len(self.south_east[0])):
                if self.south_east[i][j] ==1 and (i,j) not in list_node:
                    list_node.add((i,j))
                    file.write('    \\draw ('+str(j)+','+str(i)+')')
                    m = i
                    n = j
                    while m < len(self.south_east)-1 and n <len(self.south_east[0])-1:
                        n = n + 1
                        m = m + 1
                        if self.south_east[m][n] == 1:
                            list_node.add((m,n))
                        else:
                            break
                    if self.south_east[m][n] == 1:
                        m = m + 1
                        n = n + 1
                    file.write(' -- ('+str(n)+','+str(m)+');\n')
        list_node = set()
        file.write('% West to East lines\n')
        list_node = set()
        for i in range(len(self.east)):
            for j in range(len(self.east[0])):
                if self.east[i][j] ==1 and (i,j) not in list_node:
                    list_node.add((i,j))
                    file.write('    \\draw ('+str(j)+','+str(i)+')')
                    m = j
                    while m != len(self.east[0])-1:
                        m = m+1
                        if self.east[i][m] == 1:
                            list_node.add((i,m))
                        else:
                            break
                    if self.east[i][m] == 1:
                        m = m + 1
                    file.write(' -- ('+str(m)+','+str(i)+');\n')
        list_node = set()
        file.write('% South-West to North-East lines\n')
        list_node = set()
        new_list =[]
        for i in range(len(self.north_east)-1,-1,-1):
            for j in range(len(self.north_east[0])):
                if self.north_east[i][j] == 1 and (i,j) not in list_node:
                    list_node.add((i,j))
                    m = i
                    n = j
                    while True:
                        m = m - 1
                        n = n + 1
                        if self.north_east[m][n] == 1:
                            list_node.add((m,n))
                        else:
                            break
                    new_list.append(((i,j),(m,n)))
        new_list.sort()
        for i in range(len(new_list)):
            (x,y) = new_list[i][0]
            (p,q) = new_list[i][1]
            file.write('    \\draw ('+str(y)+','+str(x)+')')
            file.write(' -- ('+str(q)+','+str(p)+');\n')
        list_node = set()
            #end 
        file.write('\\end{tikzpicture}\n')
        file.write('\\end{center}\n')
        file.write('\\vspace*{\\fill}\n')
        file.write('\n')
        file.write('\\end{document}\n')
        file.close()


'''
frieze = Frieze('frieze_7.txt')
frieze.analyse()
frieze.display()
# In[5]:

s =[0,1,2,3,4,5,6,7]
s1=s[0:4]
s2=s[4:8]
(s1)
'''
