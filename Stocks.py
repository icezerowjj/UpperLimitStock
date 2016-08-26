# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 00:47:46 2016

@author: William
"""

from numpy import *
import pandas as pd

#Load the data
def load_hushen300(file_name):
    dataSet = pd.read_csv(file_name, delim_whitespace = True, header = None)
    return dataSet

#Clean data without nan
def get_Clean_Data(dataSet, threshold = 0.2):
    rows = shape(dataSet)[0]
    cols = shape(dataSet)[1]
    #Define a vector to store whether this row will be kept
    keep_yes = zeros(rows)
    for i in xrange(rows):
        temp = dataSet.iloc[i,:]
        row_missing = (pd.isnull(temp)).sum()
        if float(row_missing)/cols <= threshold:
            keep_yes[i] = 1
        else:
            keep_yes[i] = 0
    #Find the first time it satisfies our requirement
    for i in xrange(rows):
        if keep_yes[i] == 1.0:
            first_time = i
            break
    #Clean all the nans
    nans = pd.isnull(dataSet.iloc[first_time,:])
    nans = pd.DataFrame(nans)
    to_be_deleted = nans.any(1).nonzero()[0]
    data_nonan = dataSet.drop(to_be_deleted,1)
    data_nonan = data_nonan.fillna(0)
    return data_nonan

#Find that whether stock price rises to limit
def rise_Limit_Count_perday(data_nonan, interval, days, stock_num, point):
    count_stk_rise_limit = zeros(len(days)) 
    count_stk_rise_point = zeros(len(days)) 
    #Traverse the days
    for d in xrange(len(days)):
        #Select the transaction data within that day into temp_d
        temp_d = data_nonan.iloc[d*242:(d+1)*242,:]
        temp_d = pd.DataFrame.reset_index(temp_d)
        count1 = 0
        count2 = 0
        #Traverse the stocks
        for s in xrange(stock_num):
            #Select the transaction data of that stock into temp_d_s
            temp_d_s = temp_d.iloc[:,s]
#            temp_d_s = pd.DataFrame.reset_index(temp_d_s)
            open_price = temp_d_s[0]
            #Traverse the transaction prices
            for i in xrange(interval-1):
                #If it reaches the set point of rising 
                if temp_d_s[i]/open_price - 1 >= point:
                    count2 += 1
                    for j in xrange(i+1,interval):
                        #Judge whether it has finally reached the rise_limit point
                        if temp_d_s[j]/open_price - 1 >= 0.095:
                            count1 += 1
                            break
                        else:
                            continue
                    break
                else:
                    continue          
        count_stk_rise_limit[d] = count1
        count_stk_rise_point[d] = count2
    return count_stk_rise_limit, count_stk_rise_point

#Calculate the probability   
def calc_Prob(count_stk_rise_limit, count_stk_rise_point, days):
    Prob = zeros(len(days))
    for i in xrange(len(days)):
        nemo = count_stk_rise_limit[i]
        denom = count_stk_rise_point[i]
        Prob[i] = nemo/denom
    return Prob