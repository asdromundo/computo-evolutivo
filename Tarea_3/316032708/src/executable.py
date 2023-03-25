import sys
import pandas as pd 


import knapsack as kp
import knapsack_reader as kr

import hill_climbing as hc 
import iterative_local_search as ils 


if __name__ == '__main__': 

    

    paths = ['/data/ejeL14n45.txt', '/data/eje1n1000.txt']#
    
    
    exemplars = [ kr.read_knapsack_file(paths[i]) for i in range(len(paths)) ]


    dic_exemplars = dict()
    for i in range(len(exemplars)):
        dic_exemplars[i] = exemplars[i]


    n, c, ids, vals, ws = dic_exemplars[int(sys.argv[1])]
    
    
    data = [[ids[i], vals[i], ws[i]] for i in range(len(ids))]
    #max_benefit = sum(d[1] for d in data)
    #print(max_benefit)    

    print(ils.iterative_local_search(data,1000,c))