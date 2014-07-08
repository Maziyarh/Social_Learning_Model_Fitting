'''
Created on Feb 10, 2014

@author: Maziyar
'''
'''
Created on Jan 24, 2014

@author: maziyarh
'''
import re
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

ctr = 0
dtr = 0
filepath = 'C:\\Users\\Maziyar\\Dropbox\\Ph.D. Papers\\actions.txt'
filepath_t = 'C:\\Users\\Maziyar\\Dropbox\\Ph.D. Papers\\dataincest.txt'
filehandle = open(filepath, 'r')
data = filehandle.read()
founddata = re.split('[\n]+', data)
for line in founddata:
    ctr +=1
    incest_flag = False
    if len(line) > 4:
        match1 = re.search(r'0 0 1 0 0', line)
        match2 = re.search(r'0 1 1 0 0', line)
        match5 = re.search(r'0 0 0 0 0', line)
        match6 = re.search(r'0 1 0 0 0', line)
        match7 = re.search(r'1 0 1 1 1', line)
        match8 = re.search(r'1 1 1 1 1', line)
        match3 = re.search(r'1 0 0 1 1', line)
        match4 = re.search(r'1 1 0 1 1', line)
        if match1 or match2 or match3 or match4 or match5 or match6 or match7 or match8:
            dtr +=1
            incest_flag = True
        with open(filepath_t,"a") as outfile_t:
            outfile_t.write("Exp. %s Data incest"%ctr)
            if not incest_flag:
                outfile_t.write(" does not")
            outfile_t.write(" occur\n")
print dtr
                
        
            