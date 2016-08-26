# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 01:03:18 2016

@author: William
"""
from numpy import *
import Stocks as STK
import pandas as pd
import time

if __name__ == '__main__':
    
    #Start time
    start_time = time.clock()
    
    #Load the data
    file_name = 'mat300.txt'
    dataSet = STK.load_hushen300(file_name)
    interval = 242
    
#    #Select the last 2 days of data to process
#    test_data = dataSet.iloc[-2*interval:,:]
    
    #Using whole data
    test_data = dataSet
    
    #Reset indexing
    test_data = pd.DataFrame.reset_index(test_data)
    test_data = test_data.drop('index', 1)
    
    #Clean the data to handled
    data_nonan = STK.get_Clean_Data(test_data)
    days = range(shape(data_nonan)[0]/interval)
    stock_num = shape(data_nonan)[1]
    
    #Main function
    point = 0.09
    count_stk_rise_limit,count_stk_rise_point  = STK.rise_Limit_Count_perday(data_nonan, \
                                                    interval, days, stock_num, point)
   
    #Probability of making sense
    Prob = STK.calc_Prob(count_stk_rise_limit, count_stk_rise_point, days)
    Prob = pd.DataFrame(Prob)
#    Prob.to_excel('C:\E\Py_Files\Stocks_zhangting\Results\Prob_results.xlsx')
    #Write out to excels
    count_stk_rise_limit = pd.DataFrame(count_stk_rise_limit)
#    count_stk_rise_limit.to_excel('C:\E\Py_Files\Stocks_zhangting\Results\count_rise_limit.xlsx')
    count_stk_rise_point = pd.DataFrame(count_stk_rise_limit)
#    count_stk_rise_point.to_excel('C:\E\Py_Files\Stocks_zhangting\Results\count_rise_point.xlsx')
    
    #End time
    end_time = time.clock()
    print 'Time used is: ', end_time - start_time, 's'
    
