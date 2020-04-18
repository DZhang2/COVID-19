import numpy as np
import pandas as pd
import os
import csv
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression

os.chdir('./cleaned_data/daily/states')
states_files = os.listdir('.')
#make sure .DS_Store and other files not accounted for
state_ts = []
first = True
#analyze mortality rates first
for state in states_files:
    if state[0] != '(':
        continue
    with open(f'{state}') as infile:
        data = csv.reader(infile)
        data = list(reader)[1:]
    st = [line[0] for line in data]
    mr = [line[3] for line in data]
    if first:
        state_ts.append(st)
        state_ts.append(mr)
        first = False
    else:
        for s in st:
            for i in range(len(state_ts[0])):
                
        
    


