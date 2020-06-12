# Data graphs

import matplotlib.pyplot as plt
#import xlrd 

with open('kalman.txt') as f:
    lines = f.readlines()
    x_k = [float(line.split()[0]) for line in lines]

with open('sensor.txt') as f:
    lines = f.readlines()
    x_s = [float(line.split()[0]) for line in lines]

with open('mean.txt') as f:
    lines = f.readlines()
    x_m = [float(line.split()[0]) for line in lines]

with open('lowpass.txt') as f:
    lines = f.readlines()
    x_l = [float(line.split()[0]) for line in lines]


"""   # For some testing.
loc = ("expo.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 

arr=[]
for i in range(sheet.nrows): 
    x_e=sheet.cell_value(i,1)
    arr.append(x_e)
arr2=[]
for i in range(sheet.nrows): 
    x_e2=sheet.cell_value(i,2)
    arr2.append(x_e2)
arr3= []
for i in range(sheet.nrows): 
    x_e3=sheet.cell_value(i,3)
    arr3.append(x_e3)
"""  

#plt.xlim([0, 1000]) 
plt.ylim([0, 30]) 

plt.plot(x_k,color="red",linewidth="1",label="Kalman")
plt.plot(x_s,color="blue",linewidth="1",label="Sensor Value")
plt.plot(x_m,color="green",linewidth="1",label="Mean")
plt.plot(x_l,color="black",linewidth="1",label="Low-Pass")

plt.xlabel('Data')
plt.ylabel('Distance (cm)')
plt.title("Graph")
plt.legend()

plt.show()
