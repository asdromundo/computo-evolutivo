import sys
import pandas as pd 


import knapsack as kp
import knapsack_reader as kr

import hill_climbing as hc 
import iterative_local_search as ils 


if __name__ == '__main__': 

    

    paths = ['/data/ejeL14n45.txt', '/data/eje1n1000.txt', '/data/eje2n1000.txt']#
    
    
    exemplars = [ kr.read_knapsack_file(paths[i]) for i in range(len(paths)) ]


    dic_exemplars = dict()
    for i in range(len(exemplars)):
        dic_exemplars[i] = exemplars[i]


    #Se indica que ejemplar leer 
    n, c, ids, vals, ws = dic_exemplars[int(sys.argv[1])]
    
    #Se indica cuantas iteraciones 
    iterations  = int(sys.argv[2])

    #Se indica que perturbacion utilizar 
    # 1 : Se usa perturbacion por frecuencias 
    # 0 : Perturbacion aleatoria 
    mode_perturbation  = int(sys.argv[3])
    
    #Se indica la fuerza de perturbacion (eta) que está entre (0,1)
    eta = float(sys.argv[4]) 


    data = [[ids[i], vals[i], ws[i]] for i in range(len(ids))]
    

    print(c)
    print(">>>>>>>>------------<<<<<<<<<<<")
    print(ils.iterative_local_search(data,iterations,c,mode_perturbation,eta,10))

    #Ejemplo 
    #python3 src/executable.py 0 1000 1 .2 