import sys
import pandas as pd 


import knapsack as kp
import knapsack_reader as kr



if __name__ == '__main__': 

    

    paths = ['/data/ejeL14n45.txt']#
    
    
    exemplars = [ kr.read_knapsack_file(paths[i]) for i in range(len(paths)) ]


    dic_exemplars = dict()
    for i in range(len(exemplars)):
        dic_exemplars[i] = exemplars[i]


    n, c, ids, vals, ws = dic_exemplars[int(sys.argv[1])]

    data = [[ids[i], vals[i], ws[i]] for i in range(len(ids))]
    max_benefit = sum(d[1] for d in data)
    #print(max_benefit)    

    sol = kp.generate_random_sol(data)
    print(sol)
    print(kp.evaluate(sol,max_benefit))
    print(">>>>>>>>")

    best_neighbor = kp.neighborhood_operator(sol,c,max_benefit,8)
    print(best_neighbor)
    print(kp.evaluate(best_neighbor,max_benefit))

