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
    

    sol = kp.generate_random_sol(data)
    print(sol)
    print(sol.carried_items+sol.no_carried_items == data)    

    print(">>>>>>>>>>")

    temp_1 = set([tuple(lst) for lst in sol.carried_items+sol.no_carried_items])
    temp_2 = set([tuple(lst) for lst in data])
    diff = [list(item) for item in temp_1 - temp_2]

    print(diff)
    print(">>>>>>>>>>")

    print("----------------")

    neighbor = kp.neighborOperator(sol, c)
    print(neighbor)
    print(">>>>>>>>>>")

    temp_1 = set([tuple(lst) for lst in neighbor.carried_items+neighbor.no_carried_items])
    temp_2 = set([tuple(lst) for lst in data])
    diff = [list(item) for item in temp_1 - temp_2]

    print(diff)
    print(">>>>>>>>>>")
    print(len(neighbor.carried_items+neighbor.no_carried_items) == len(data))