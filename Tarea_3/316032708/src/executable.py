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

def generate_avg_evol(data,iterations,hill_iterations,c,eta,temp,repetitions, w_one_path, w_best_path):

    #Para la perturbacion aleatoria 
    avg_fitness_rand = [] ## Aqui vamos a guardar cada arreglo de evolucion de fitness 
    avg_evol_rand = [] ## Aqui guardamos las tuplas [iter_fraccion, fitness_in_that_moment]
    avg_iters_rand = [] 
    bests_rand= [] ##Todas las soluciones

    #Para la perturbacion por frecuencias 
    avg_fitness_frec = [] ## Aqui vamos a guardar cada arreglo de evolucion de fitness 
    avg_evol_frec = [] ## Aqui guardamos las tuplas [iter_fraccion, fitness_in_that_moment]
    avg_iters_frec = [] 
    bests_frec= [] ##Todas las soluciones 

    for i in range(repetitions):
        
        sol, fitness_data, iter_data, avg_data = ils.iterative_local_search(data,iterations,hill_iterations,c,0,eta,temp)
        
        avg_fitness_rand.append(fitness_data)####
        avg_evol_rand.append(avg_data)#
        avg_iters_rand.append(iter_data)
        bests_rand.append(sol)

        sol_f, fitness_data_f, iter_data_f, avg_data_f = ils.iterative_local_search(data,iterations,hill_iterations,c,1,eta,temp)

        avg_fitness_frec.append(fitness_data_f)
        avg_evol_frec.append(avg_data_f)#
        avg_iters_frec.append(iter_data_f)
        bests_frec.append(sol_f)


    #PARA PERTURBACION ALEATORIA 
    #Tenemos que graficar los datos promedios 
    avr_evol_fit_data_r = []
    for i in range(len(avg_evol_rand[0])):
        avr_evol_fit_data_r.append([d[i][1] for d in avg_evol_rand])
        
    avr_evol_fit_total_r = []
    for arr in avr_evol_fit_data_r :
        avr_evol_fit_total_r.append(sum(arr)/len(arr))

    #Obtenemos las iteraciones 
    avr_evol_iter_total_r = [x[0] for x in avg_evol_rand[0]]
   

    #PARA PERTURBACION POR FRECUENCIAS 
    avr_evol_fit_data_f = []
    for i in range(len(avg_evol_frec[0])):
        avr_evol_fit_data_f.append([d[i][1] for d in avg_evol_frec])
        
    avr_evol_fit_total_f = []
    for arr in avr_evol_fit_data_f :
        avr_evol_fit_total_f.append(sum(arr)/len(arr))

    #Obtenemos las iteraciones 
    avr_evol_iter_total_f = [x[0] for x in avg_evol_frec[0]]
    

   
    #Ahora tenemos que obtener al mejor, el promedio, el peor y la desviacion estandar de esas 30 iteraciones
    data_from_best_rand = [s.fitness_value for s in bests_rand]

    #Encontramos a la mejor 
    best_random_sol = bests_rand[0]
    for sol in bests_rand:
        if sol.fitness_value <= best_random_sol.fitness_value:
            best_random_sol = sol 

    #Escribimos la mejor  
    kr.write_knapsack_file(w_one_path, [str(best_random_sol)])

    #Guardamos el los arreglos con los mejores valores 
    kr.write_knapsack_file(w_best_path, [str(data_from_best_rand)])        

    #plt.show()
    df_r = pd.DataFrame({"Fitness" : data_from_best_rand})
    #print(df_r["Fitness"].std())
    print(df_r.describe())

    
    plt.plot(avr_evol_iter_total_r,avr_evol_fit_total_r,marker= 'o')
    plt.plot(avr_evol_iter_total_f,avr_evol_fit_total_f,marker= '*')
    
    plt.show()
    


if __name__ == '__main__': 

    

    paths = ['/data/ejeL14n45.txt', # 0
             '/data/ejeknapPI_3_200_1000_14.txt', # 1 
              '/data/eje1n1000.txt', # 2
              '/data/eje2n1000.txt', # 3
              '/data/n_1000_c_1000000_g_6_f_0.3_eps_0.001_s_100.txt']#4

    w_paths_one_sol = ['/output/ejeL14n45.txt', # 0
                        '/output/ejeknapPI_3_200_1000_14.txt', # 1 
                        '/output/eje1n1000.txt', # 2
                        '/output/eje2n1000.txt', # 3
                        '/output/n_1000_c_1000000_g_6_f_0.3_eps_0.001_s_100.txt']#4

    w_paths_best_sols = ['/output/best_sols/bs_ejeL14n45.txt', # 0
                        '/output/best_sols/bs_ejeknapPI_3_200_1000_14.txt', # 1 
                        '/output/best_sols/bs_eje1n1000.txt', # 2
                        '/output/best_sols/bs_eje2n1000.txt', # 3
                        '/output/best_sols/bs_n_1000_c_1000000_g_6_f_0.3_eps_0.001_s_100.txt']#4

    
    
    exemplars = [ kr.read_knapsack_file(paths[i]) for i in range(len(paths)) ]


    dic_exemplars = dict()
    for i in range(len(exemplars)):
        dic_exemplars[i] = exemplars[i]


    #Se indica que ejemplar leer 
    n, c, ids, vals, ws = dic_exemplars[int(sys.argv[1])]
    
    #Se indica el archivo para guardar la mejor solucion encontrada  
    w_paths_one_sol = w_paths_one_sol[int(sys.argv[1])]

    #Se indica el archivo para guardar los valores de las mejores soluciones encontradas en x repeticiones
    w_paths_best_sols = w_paths_best_sols[int(sys.argv[1])]

    #kr.write_knapsack_file(w_paths[int(sys.argv[1])], w_data)

    #Se indica cuantas iteraciones para ILS 
    iterations  = int(sys.argv[2])

    #Se indica cuantas iteraciones para Hill Climbing
    hill_iterations = int(sys.argv[3])

    #Se indica que perturbacion utilizar 
    # 1 : Se usa perturbacion por frecuencias 
    # 0 : Perturbacion aleatoria 
    mode_perturbation  = int(sys.argv[4])
    
    #Se indica la fuerza de perturbacion (eta) que está entre (0,1)
    eta = float(sys.argv[5]) 


    data = [[ids[i], vals[i], ws[i]] for i in range(len(ids))]
    

    #sol, fitness_data, iter_data, avg_evol = ils.iterative_local_search(data,iterations,hill_iterations,c,0,eta,10)
    #print(avg_evol)
    #sol_1, fitness_data_1, iter_data_1, avg_evol_1 = ils.iterative_local_search(data,iterations,hill_iterations,c,1,eta,10)
    #print(avg_evol_1)
    #print(">>>>>>>>------------<<<<<<<<<<<")
    #print(sol)

    #draw_graph_pertubations_comparations(paths[int(sys.argv[1])], eta, [iter_data,fitness_data],[iter_data_1,fitness_data_1],n,[sol.fitness_value, sol_1.fitness_value])

    generate_avg_evol(data,200,50,c,eta,10,30,w_paths_one_sol,w_paths_best_sols)

    
    
    
     