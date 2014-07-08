'''
Created on Jan 16, 2014

@author: maziyarh
'''
import numpy as np
import matplotlib.pyplot as plt
import re

filepath = 'C:\\Users\\maziyarh\\Documents\\My Dropbox\\Ph.D. Papers\\allData.txt'
Actions_A =  np.array([0,0,0,0,0])
Actions_B =  np.array([0,0,0,0,0])
Actions = np.array([0,0])
Trial_no_A = 0
Trial_no_B = 0
Experiment_no = 0
ground_truth = 0

social_fail_true = 0

#reading data from .txt file
filehandle = open(filepath, 'r')
data = filehandle.read()
founddata = re.split('[\n]+', data)
for line in founddata:
    symbols = re.split('[\\s]+[\\t]*', line)
    if len(symbols) > 2:
        if symbols[0] == 'A':
            new_row = np.array([Experiment_no, Trial_no_A, int(symbols[1]),int(symbols[2]), ground_truth ])
            Actions_A = np.vstack([Actions_A, new_row])
            Actions = np.vstack([Actions, [Experiment_no, int(symbols[1]) ]])
            Trial_no_A +=1
        elif  symbols[0] == 'B':
            new_row = np.array([Experiment_no, Trial_no_B, int(symbols[1]),int(symbols[2]), ground_truth ])
            Actions_B = np.vstack([Actions_B, new_row])
            Actions = np.vstack([Actions, [Experiment_no, int(symbols[1]) ]])
            Trial_no_B += 1
        else:
            Experiment_no += 1
            ground_truth = int(symbols[2])
            Trial_no_A = 1
            Trial_no_B = 1
             
Experiment = input('Enter the Experiment Number: ')
index = [i for (i), value in np.ndenumerate(Actions_A[:,0]) if (value==Experiment)]
T = len(index)
print(T)
plt.figure(1)
plt.plot(Actions_A[index,1], Actions_A[index,2] + .02, 'b', label="Sample Path User A")
plt.plot(Actions_A[index,1], Actions_B[index,2] +.04, 'r', label="Sample Path User B")
plt.plot(Actions_A[index,1], Actions_A[index,4] + .06, 'g', label="Ground Truth")
#plt.legend(loc=1, mode="expand")
plt.title(r'Actions')
plt.show()
