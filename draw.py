'''
The code below is the code about QRTD, SQD and Box plot
Author: Judu Xu
Date: 12/04/2022
'''

import matplotlib.pyplot as plt
import os

#ABOUT THE QRTD, PATH IS THE DOCUMENT PATH WHERE CONTAINS TRACE FILE
def QRTD(path):
    
    file_name_list = os.listdir("path")

    #SET REL ERROR
    t = [0.07, 0.08, 0.09, 0.10, 0.11]
    
    d = {}
    for j in range(len(t)):
        data = []
        #READ DATA AND CHECK
        for file_name in file_name_list:
            f = open("path" + file_name, "r")
            lines = f.readlines()
            index = 4542*(1 + t[j])
            for i in lines:
                l = i.split(',')
                if float(l[1]) <= index:
                    data.append(float(l[0]))
                    break
        d[j] = sorted(data)
    
    print(d)
    
    for i in range(len(t)):
        y = []
        y.append(0)
        data = []
        data.append(d[i][0])
        for j in range(len(d[i])):
            data.append(d[i][j])
            if j != 0:
                data.append(d[i][j])
        data.append(460)
        for j in range(len(d[i])):
            y.append(0.1 * (j + 1))
            y.append(0.1 * (j + 1))
            
        plt.plot(data, y, linestyle='solid', label = str(round((t[i] * 100),2)) + '%')
        
    plt.xlabel('run_time')
    plt.ylabel('p(solve)')
    plt.legend()

#ABOUT THE SQR, PATH IS THE DOCUMENT PATH WHERE CONTAINS TRACE FILE
def SQR(path):
    
    file_name_list = os.listdir(path)

    #SET THE TIME
    t = [5, 10, 15, 20, 25]
    #SET THE REL ERROR
    rel = []
    for i in range(5):
        rel.append(i * 0.1)

    for j in range(len(t)):
        data = []
        for r in rel:
            cnt = 0
            index = 2203*(1 + r/100)
            #READ DATA AND CHECK
            for file_name in file_name_list:         
                f = open(path + file_name, "r")
                lines = f.readlines()
                for k in range(len(lines)):
                    time, v = lines[k].split(',')
                    time = float(time)
                    v = int(v)
                    if v <= index:
                        if time < t[j]:
                            cnt += 1
                        break
                f.close()

            data.append(cnt/10)
        plt.plot(rel, data, linestyle='solid', label = str(t[j]) + 's')
        
    
    plt.xlabel('relative_sol_quality(%)')
    plt.ylabel('p(solve)')
    plt.legend()

#ABOUT THE BOX PLOT, PATH IS THE DOCUMENT PATH WHERE CONTAINS TRACE FILE
def box(path1, path2):
    
    file_name_list1 = os.listdir(path1)
    file_name_list2 = os.listdir(path2)
    data1 = []
    data2 = []
    #READ DATA AND CHECK
    for file_name in file_name_list1:
        f = open(path1 + file_name, "r")
        lines = f.readlines()
        l = lines[-1].split(',')
        data1.append(float(l[0]))    
        f.close()
    #READ DATA AND CHECK
    for file_name in file_name_list2:
        f = open(path2 + file_name, "r")
        lines = f.readlines()
        l = lines[-1].split(',')
        data2.append(float(l[0]))    
        f.close()

    
    plt.boxplot(data1)
    plt.show()


    plt.boxplot(data2)
    plt.show()