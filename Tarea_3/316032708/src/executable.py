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
    #max_benefit = sum(d[1] for d in data)
    #print(max_benefit)    

    sol = kp.generate_random_sol(data)
    print(sol)
    print("Fitness :")
    print(kp.evaluate(sol))
    print("Amount items :")
    print(len(sol.carried_items))
    print(">>>>>>>>")

    best_neighbor = kp.neighborhood_operator(sol,c,2)
    print(best_neighbor)
    print("Fitness :")
    print(kp.evaluate(best_neighbor))
    print("Amount items :")
    print(len(best_neighbor.carried_items))

