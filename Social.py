'''
Created on Jan 16, 2014

@author: Maziyar
'''

import re
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

def calculateB(x,y_max,n):
    out = np.zeros((x,y_max))
    for i in range(1,x+1):
        y = sp.r_[1:y_max+1]
        z = np.exp(-np.power(y - 1 - i,2)/(2*n*n))/(n*np.sqrt(2*3.1415))
        out[i-1,:] = z/np.sum(z)
    return out

def calculateC(x,A):
    out = np.zeros((x,int(A)))
    for i in range(1,x+1):
        for j in range(0,int(A)):
            out[i-1,j] = np.absolute((4-i)*j +(1-j)*(i-1))
    return out
def ldlp(y,a,p,B,C):
    out = 0
    cost_a = np.matrix(C[:,a])*np.matrix(np.multiply(B[:,y],p)).T
    cost_a_com = np.matrix(C[:,np.absolute(1-a)])*np.matrix(np.multiply(B[:,y],p)).T
    if cost_a < cost_a_com:
        out = 1
    return out
    
    
        
    
def calculateR(x,A,p,B,C):
    out = np.zeros((x,int(A)))
    for i in range(1,x+1):
        for j in range(0,int(A)):
            out[i-1,j] = ldlp(i-1,j,p,B,C)
            
    return np.matrix(B)*np.matrix(out)
    
def new_action(R,B,C,p,x_max,y,actions):
    bel = np.ones(np.shape(p))
    if len(actions) > 1:
        bel_t =  np.multiply(R[:,actions[0]],R[:,actions[1]])
        bel = bel_t.T
    temp_bel = np.multiply(bel,p)
    normalized_temp_bel = temp_bel/np.sum(temp_bel)
    private_bel_temp = np.multiply(B[:,y],normalized_temp_bel)
    private_bel = private_bel_temp / np.sum(private_bel_temp)
    temp = np.zeros(2)
    for action in range(0,2):
        temp[action] =np.matrix(C[:,action])*np.matrix(private_bel).T
    n_action = np.argmin(temp)
    return n_action
                

# initializations
filepath = 'C:\\Users\\maziyarh\\Documents\\My Dropbox\\Ph.D. Papers\\allData.txt'
filepath2 = 'C:\\Users\\maziyarh\\Documents\\My Dropbox\\Ph.D. Papers\\outData.txt'
filepath_A = 'C:\\Users\\maziyarh\\Documents\\My Dropbox\\Ph.D. Papers\\outData_A.txt'
filepath_B = 'C:\\Users\\maziyarh\\Documents\\My Dropbox\\Ph.D. Papers\\outData_B.txt'
filepath_t = 'C:\\Users\\maziyarh\\Documents\\My Dropbox\\Ph.D. Papers\\actions.txt'
Actions_A =  np.array([0,0,0,0,0])
Actions_B =  np.array([0,0,0,0,0])
Actions = np.array([0,0])
Trial_no_A = 0
Trial_no_B = 0
Experiment_no = 0
ground_truth = 0
counter_trial_total = 0
threshold_validity = 4
threshold_herding = 4
herding_ctr = 0
herding_true_ctr = 0
social_failure = 0
social_fail_true = 0
x_max = 4
noise = 2
init_belief = np.ones((1,x_max))/x_max


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


B = calculateB(x_max,x_max, noise)
Cost = calculateC(x_max,2.)
R = calculateR(x_max,2,init_belief,B,Cost)   
#np.savetxt('User_A.txt', Actions_A)
#np.savetxt('User_B.txt', Actions_B)
Exp_tot  = np.max(Actions_A[:,0])
for j in xrange(0,Exp_tot):
    Experiment = j +1
    index = [i for (i), value in np.ndenumerate(Actions_A[:,0]) if (value==Experiment)]
    index_t = [k for (k), value in np.ndenumerate(Actions[:,0]) if (value==Experiment)]
    index_b = [z for (z), value in np.ndenumerate(Actions_B[:,0]) if (value==Experiment)]
    print "Experiment", Experiment, "..."
    Trials = len(index_t)
    if Trials > threshold_validity:
        counter_trial_total +=1
        sample_path = Actions[index_t,1]
        sample_path_A = Actions_A[index,2]
        sample_path_B = Actions_B[index_b,2]
        temp3 = sample_path_A == sample_path_A[0]*np.ones(np.shape(sample_path_A))
        check_SL_a = np.sum(temp3)
        temp4 = sample_path_B == sample_path_B[0]*np.ones(np.shape(sample_path_B))
        check_SL_b = np.sum(temp4)
        with open(filepath2,"a") as outfile:
        #    outfile.write("Experiment %s Actions:" %Experiment)
            outfile.write("Exp. %s:" %Experiment)
        with open(filepath_A,"a") as outfile_A:
            outfile_A.write("Experiment %s Actions:" %Experiment)
        with open(filepath_B,"a") as outfile_B:
            outfile_B.write("Experiment %s Actions:" %Experiment)
        temp_obs = 0.
        ctr = 0
        for i in range(0,len(sample_path)):
            actions = np.array([])
            with open(filepath_t,"a") as outfile_t:
                outfile_t.write(" %s" %int(sample_path[i]))
            if i > 1:
                actions = sample_path[i-2:i]  
            for observation in range(0,x_max):
                pot_next_action = new_action(R,B,Cost,init_belief,x_max,observation,actions)
                if pot_next_action == sample_path[i]:
                    #with open(filepath2,"a") as outfile:
                    #    outfile.write(" %s" %observation)
                    temp_obs = temp_obs + observation
                    ctr +=1
                    if i % 2 == 0:
                        with open(filepath_A,"a") as outfile_A:
                            outfile_A.write(" %s" %observation)
                    else:
                        with open(filepath_B,"a") as outfile_B:
                            outfile_B.write(" %s" %observation)
                    break
        with open(filepath_t,"a") as outfile_t:
            outfile_t.write(" \n")
        avg_obs = temp_obs/len(sample_path)
        if check_SL_a == len(temp3):
            social_failure +=1
            with open(filepath2,"a") as outfile:
                outfile.write(", Social Failure,")
            if sample_path_A[0] == Actions_A[Experiment,4]:
                social_fail_true +=1
            
        elif check_SL_b == len(temp4):
            social_failure +=1
            with open(filepath2,"a") as outfile:
                outfile.write(", Social Failure,")
            if sample_path_B[0] == Actions_B[Experiment,4]:
                social_fail_true +=1
            
        temp= len(sample_path)
        benchmark = sample_path[temp-1]
        temp2 = sample_path[temp-threshold_herding:temp] == benchmark*np.ones((threshold_herding,1))
        check= np.sum(temp2)
        if check == threshold_herding:
            herding_ctr +=1
            with open(filepath2,"a") as outfile:
                outfile.write(" Herds to")
            if benchmark == Actions_A[Experiment,4]:
                herding_true_ctr +=1
                with open(filepath2,"a") as outfile:
                    outfile.write(" True")
            else:
                with open(filepath2,"a") as outfile:
                    outfile.write(" False")
            with open(filepath2,"a") as outfile:
                outfile.write(" Value. ")
        else:
            with open(filepath2,"a") as outfile:
                outfile.write(" No Herding. ")
        with open(filepath2,"a") as outfile:
            outfile.write(" Avg. Obs.: %s"%avg_obs)
            outfile.write(" Truth: %s"%Actions_A[Experiment,4])
            outfile.write("\n")
        with open(filepath_A,"a") as outfile_A:
            outfile_A.write("\n")
        with open(filepath_B,"a") as outfile_B:
            outfile_B.write("\n")
                                
                    

                
            
print "Total Number of Valid Experiments : ", counter_trial_total, "Among ", herding_ctr, " herds, ", herding_true_ctr, 'was successful.'
print "There were ", social_failure, "social failures; Among them", social_fail_true,"was true."