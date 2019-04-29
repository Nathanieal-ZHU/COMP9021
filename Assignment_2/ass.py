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
        for i in range(2,round(len(self.data[0])/2)+1):
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
        self.dic = {}
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data[i])):
                self.dic[f'({i},{j})'] = {}
                self.dic[f'({i},{j})']['N'] = 0
                self.dic[f'({i},{j})']['E'] = 0
                self.dic[f'({i},{j})']['NE'] = 0
                self.dic[f'({i},{j})']['SE'] = 0
        self.data_2 = copy.deepcopy(self.data)
        for i in range(0,len(self.data)):
            for j in range(0, len(self.data[i])):
                if (self.data_2[i][j] - 8) >= 0:
                    self.dic[f'({i},{j})']['SE'] = 1
                    self.data_2[i][j] = self.data_2[i][j] - 8
                if (self.data_2[i][j] - 4) >= 0:
                    self.dic[f'({i},{j})']['E'] = 1
                    self.data_2[i][j] = self.data_2[i][j] - 4
                if (self.data_2[i][j] - 2) >= 0:
                    self.dic[f'({i},{j})']['NE'] = 1
                    self.data_2[i][j] = self.data_2[i][j] - 2
                if (self.data_2[i][j] - 1) == 0:
                    self.dic[f'({i},{j})']['N'] = 1
        for i in range(0,len(self.data)-1):
            for j in range(0,len(self.data[i])):
                if self.dic[f'({i},{j})']['SE'] == 1:
                    if self.dic[f'({i+1},{j})']['NE'] ==1:
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
            self.vflag = False
            self.rflag = False
            for i in range(self.period):
                for j in range(self.length):
                    for m in range(len(self.data)):
                        self.vflag = True
                        if self.dic[f'({m},{i+j})']['E'] != self.dic[f'({m},{self.period-1-j+i})']['E']:
                            self.vflag = False
                            break
                        if m > 0:
                            if self.dic[f'({m},{i+j})']['N'] != self.dic[f'({m},{self.period-j+i})']['N']:
                                self.vflag = False
                                break
                            if self.dic[f'({m},{i+j})']['NE'] != self.dic[f'({m-1},{self.period-1-j+i})']['SE']:
                                self.vflag = False
                                break
                        if m <len(self.data)-1:
                            if self.dic[f'({m},{i+j})']['SE'] != self.dic[f'({m+1},{self.period-1-j+i})']['NE']:
                                self.vflag = False
                                break
                    if self.vflag == False:
                        break
                if self.vflag == True:
                    return True
            if self.rflag == False:
                self.apflag = True
                self.period =self.period + 1
        if self.period % 2 == 1:
            self.vflag = False
            self.length = int(self.period/2)
            for i in range(self.period):
                for j in range(self.length+1):
                    for m in range(len(self.data)):
                        self.vflag = True
                        if self.dic[f'({m},{i+j})']['E'] != self.dic[f'({m},{self.period-1-j+i})']['E']:
                            self.vflag = False
                            break
                        if m >0:
                            if self.dic[f'({m},{i+j})']['N'] != self.dic[f'({m},{self.period-j+i})']['N']:
                                self.vflag = False
                                break
                            if self.dic[f'({m},{i+j})']['NE'] != self.dic[f'({m-1},{self.period-1-j+i})']['SE']:
                                self.vflag = False
                                break
                        if m < len(self.data)-1:
                            if self.dic[f'({m},{i+j})']['SE'] != self.dic[f'({m+1},{self.period-1-j+i})']['NE']:
                                self.vflag = False
                                break
                    if self.vflag == False:
                        break
                if self.vflag == True:
                    if self.apflag == True:
                        self.period = self.period -1
                    return True
            if self.apflag==True:
                self.period =self.period - 1
        return False
        
    def horizontal(self):
        self.height = len(self.data)
        if self.height % 2 == 0:
            self.hflag = False
            self.length = int(self.height/2)
            for i in range(self.length+1):
                for j in range(self.period):
                    self.hflag = True
                    if self.dic[f'({i},{j})']['E'] != self.dic[f'({self.height-1-i},{j})']['E']:
                        self.hflag = False
                        break
                    if i > 0:
                        if self.dic[f'({i},{j})']['N'] != self.dic[f'({self.height-i},{j})']['N']:
                            self.hflag = False
                            break
                        if self.dic[f'({i},{j})']['NE'] != self.dic[f'({self.height-1-i},{j})']['SE']:
                            self.hflag =False
                            break
                    if i < self.height-1:
                        if self.dic[f'({i},{j})']['SE'] != self.dic[f'({self.height-1-i},{j})']['NE']:
                            self.hflag = False
                            break
                if self.hflag == False:
                    break
            if self.hflag == True:
                return True
        if self.height % 2 == 1:
            self.hflag = False
            for i in range(self.height):
                for j in range(self.period):
                    self.hflag = True
                    if self.dic[f'({i},{j})']['E'] != self.dic[f'({self.height-1-i},{j})']['E']:
                        self.hflag = False
                        break
                    if i > 0:
                        if self.dic[f'({i},{j})']['N'] != self.dic[f'({self.height-i},{j})']['N']:
                            self.hflag = False
                            break
                        if self.dic[f'({i},{j})']['NE'] != self.dic[f'({self.height-1-i},{j})']['SE']:
                            self.hflag =False
                            break
                    if i < self.height-1:
                        if self.dic[f'({i},{j})']['SE'] != self.dic[f'({self.height-1-i},{j})']['NE']:
                            self.hflag = False
                            break
                if self.hflag == False:
                    break
            if self.hflag == True:
                return True
        return False
            
    def glided_horizontal(self):
        self.height = len(self.data)
        if self.period % 2 == 1:
            return False
        if self.period % 2 == 0:
            self.pd = int(self.period/2)
            self.ghflag = False
            for i in range(self.period):
                for j in range(self.pd):
                    for m in range(self.height):
                        self.ghflag = True
                        if self.dic[f'({m},{j+i})']['E'] != self.dic[f'({self.height-1-m},{j+i+self.pd})']['E']:
                            self.ghflag = False
                            break
                        if m > 0:
                            if self.dic[f'({m},{j+i})']['N'] != self.dic[f'({self.height-m},{j+i+self.pd})']['N']:
                                self.ghflag = False
                                break
                            if self.dic[f'({m},{j+i})']['NE'] != self.dic[f'({self.height-1-m},{j+i+self.pd})']['SE']:
                                self.ghflag =False
                                break
                        if m < self.height-1:
                            if self.dic[f'({m},{j+i})']['SE'] != self.dic[f'({self.height-1-m},{j+i+self.pd})']['NE']:
                                self.ghflag = False
                                break
                    if self.ghflag == False:
                        break
            if self.ghflag == True:
                return True
        return False
    
    def rotation(self):
        self.height = len(self.data)
        for i in range(self.period):
            for j in range(self.height):
                for m in range(self.period):
                    self.rflag = True
                    if j > 0:
                        if self.dic[f'({j},{m+i})']['N'] != self.dic[f'({self.height-j},{i+self.period-m})']['N']:
                            self.rflag = False
                            break  
                        if self.dic[f'({j},{m+i})']['NE'] != self.dic[f'({self.height-j},{i+self.period-1-m})']['NE']:
                            break
                    if self.dic[f'({j},{m+i})']['E'] != self.dic[f'({self.height-1-j},{i+self.period-1-m})']['E']:
                        self.rflag = False
                        break
                    if j < self.height-1:
                        if self.dic[f'({j},{m+i})']['SE'] != self.dic[f'({self.height-2-j},{i+self.period-1-m})']['SE']:
                            self.rflag = False
                            break
                if self.rflag == False:
                    break
            if self.rflag == True:
                    return True
        self.period =self.period + 1
        for i in range(self.period):
            for j in range(self.height):
                for m in range(self.period):
                    self.rflag = True
                    if j > 0:
                        if self.dic[f'({j},{m+i})']['N'] != self.dic[f'({self.height-j},{i+self.period-m})']['N']:
                            self.rflag = False
                            break  
                        if self.dic[f'({j},{m+i})']['NE'] != self.dic[f'({self.height-j},{i+self.period-1-m})']['NE']:
                            break
                    if self.dic[f'({j},{m+i})']['E'] != self.dic[f'({self.height-1-j},{i+self.period-1-m})']['E']:
                        self.rflag = False
                        break
                    if j < self.height-1:
                        if self.dic[f'({j},{m+i})']['SE'] != self.dic[f'({self.height-2-j},{i+self.period-1-m})']['SE']:
                            self.rflag = False
                            break
                if self.rflag == False:
                    break
            if self.rflag == True:
                self.period = self.period -1
                return True
        self.period= self.period -1
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
        for i in range(len(self.data[0])):
            for j in range(len(self.data)):
                if self.dic[f'({j},{i})']['N'] == 1 and (j,i) not in list_node:
                    list_node.add((j,i))
                    file.write('    \\draw ('+str(i)+','+str(j-1)+')')
                    m = j
                    while m < len(self.data)-1:
                        m = m + 1
                        if self.dic[f'({m},{i})']['N'] == 1:
                            list_node.add((m,i))
                        else:
                            break
                    if self.dic[f'({m},{i})']['N'] == 1:
                        m= m+1
                    file.write(' -- ('+str(i)+','+str(m-1)+');\n')    
        list_node = set()
        file.write('% North-West to South-East lines\n')
        list_node = set()
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.dic[f'({i},{j})']['SE'] ==1 and (i,j) not in list_node:
                    list_node.add((i,j))
                    file.write('    \\draw ('+str(j)+','+str(i)+')')
                    m = i
                    n = j
                    while m < len(self.data)-1 and n <len(self.data[0])-1:
                        n = n + 1
                        m = m + 1
                        if self.dic[f'({m},{n})']['SE'] == 1:
                            list_node.add((m,n))
                        else:
                            break
                    if self.dic[f'({m},{n})']['SE'] == 1:
                        m = m + 1
                        n = n + 1
                    file.write(' -- ('+str(n)+','+str(m)+');\n') 
        list_node = set()
        file.write('% West to East lines\n')
        list_node = set()
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.dic[f'({i},{j})']['E'] == 1 and (i,j) not in list_node:
                    list_node.add((i,j))
                    file.write('    \\draw ('+str(j)+','+str(i)+')')
                    m = j
                    while m != len(self.data[0])-1:
                        m = m+1
                        if self.dic[f'({i},{m})']['E'] == 1:
                            list_node.add((i,m))
                        else:
                            break
                    if self.dic[f'({i},{m})']['E'] == 1:
                        m = m + 1
                    file.write(' -- ('+str(m)+','+str(i)+');\n')
        list_node = set()
        file.write('% South-West to North-East lines\n')
        list_node = set()
        new_list =[]
        for i in range(len(self.data)-1,-1,-1):
            for j in range(len(self.data[0])):
                if self.dic[f'({i},{j})']['NE'] == 1 and (i,j) not in list_node:
                    list_node.add((i,j))
                    m = i
                    n = j
                    while m != 0 or n != len(self.data[0])-1:
                        m = m - 1
                        n = n + 1
                        if self.dic[f'({m},{n})']['NE'] == 1:
                            list_node.add((m,n))
                        else:
                            break
                    if self.dic[f'({m},{n})']['NE'] == 1:
                        m = m-1
                        n = n+1
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
                           
frieze = Frieze('frieze_1.txt')
frieze.analyse()
frieze.display()



