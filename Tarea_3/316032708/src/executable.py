import sys
import pandas as pd
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
import knapsack as kp
import knapsack_reader as kr

import hill_climbing as hc 
import iterative_local_search as ils 



def draw_graph_pertubations_comparations(name, eta,  data_1, data_2, size,best):

    plt.plot(data_1[0],data_1[1])
    plt.plot(data_2[0],data_2[1])

    plt.title("Nombre : {} \nTamanio ejemplar : {} \nFuerza de Perturbacion : {} \nMejor Solucion por perturbacion aleatoria: {}\nMejor Solucion por perturbacion por Frecuencia: {} ".format(name,size,eta,best[0],best[1]), loc = 'left')
    plt.xlabel("iterations")
    plt.ylabel("Fitness")
    plt.legend(['Random Perturbation', 'Frecuency Perturbation'])
    plt.show()

def generate_avg_evol(data,iterations,hill_iterations,c,eta,temp,repetitions):
    sol, fitness_data, iter_data, avg_data = ils.iterative_local_search(data,iterations,hill_iterations,c,0,eta,temp,repetitions)
    sol, fitness_data, iter_data, avg_data = ils.iterative_local_search(data,iterations,hill_iterations,c,1,eta,temp,repetitions)









if __name__ == '__main__': 

    

    paths = ['/data/ejeL14n45.txt', # 0
             '/data/ejeknapPI_3_200_1000_14.txt', # 1 
              '/data/eje1n1000.txt', # 2
              '/data/eje2n1000.txt', # 3
              '/data/n_1000_c_1000000_g_6_f_0.3_eps_0.001_s_100.txt']#4

    w_paths = ['/output/ejeL14n45.txt', # 0
             '/output/ejeknapPI_3_200_1000_14.txt', # 1 
              '/output/eje1n1000.txt', # 2
              '/output/eje2n1000.txt', # 3
              '/output/n_1000_c_1000000_g_6_f_0.3_eps_0.001_s_100.txt']#4

    
    
    exemplars = [ kr.read_knapsack_file(paths[i]) for i in range(len(paths)) ]


    dic_exemplars = dict()
    for i in range(len(exemplars)):
        dic_exemplars[i] = exemplars[i]


    #Se indica que ejemplar leer 
    n, c, ids, vals, ws = dic_exemplars[int(sys.argv[1])]
    
    #Se indica el archivo para guardar la solucion 
    #kr.write_knapsack_file(w_paths[int(sys.argv[1])], w_data)

    #Se indica cuantas iteraciones 
    iterations  = int(sys.argv[2])

    hill_iterations = int(sys.argv[3])

    #Se indica que perturbacion utilizar 
    # 1 : Se usa perturbacion por frecuencias 
    # 0 : Perturbacion aleatoria 
    mode_perturbation  = int(sys.argv[4])
    
    #Se indica la fuerza de perturbacion (eta) que está entre (0,1)
    eta = float(sys.argv[5]) 


    data = [[ids[i], vals[i], ws[i]] for i in range(len(ids))]
    

    sol, fitness_data, iter_data, avg_evol = ils.iterative_local_search(data,iterations,hill_iterations,c,0,eta,10)
    print(avg_evol)
    sol_1, fitness_data_1, iter_data_1, avg_evol_1 = ils.iterative_local_search(data,iterations,hill_iterations,c,1,eta,10)
    print(avg_evol_1)
    #print(">>>>>>>>------------<<<<<<<<<<<")
    #print(sol)

    draw_graph_pertubations_comparations(paths[int(sys.argv[1])], eta, [iter_data,fitness_data],[iter_data_1,fitness_data_1],n,[sol.fitness_value, sol_1.fitness_value])

    

    
    
    
     