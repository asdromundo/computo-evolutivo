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
from scipy import stats
from scipy.stats import levene
from scipy.stats import f_oneway


def draw_graph_pertubations_comparations(name, eta,  data_1, data_2, size,best):

    plt.plot(data_1[0],data_1[1])
    plt.plot(data_2[0],data_2[1])

    plt.title("Nombre : {} \nTamanio ejemplar : {} \nFuerza de Perturbacion : {} \nMejor Solucion por perturbacion aleatoria: {}\nMejor Solucion por perturbacion por Frecuencia: {} ".format(name,size,eta,best[0],best[1]), loc = 'left')
    plt.xlabel("iterations")
    plt.ylabel("Fitness")
    plt.legend(['Random Perturbation', 'Frecuency Perturbation'])
    plt.show()

def generate_avg_evol(data,iterations,hill_iterations,c,eta,temp,repetitions, w_one_path, w_best_path,instance_name):

    '''
    Esta funcion se encarga de generar los datos necesarios para mostrar la evolucion promedio del algoritmo ITS. 
    Asimismo, obtiene las mejores soluciones obtenidas en las 30 repeticiones del algoritmo y las guarda en el archivo 
    output/best_sols/nombre_ejemplar.txt, estos valores son utilizados para obtener las pruebas de hipotesis y los boxplot. 

    Args: 

    data : datos del ejemplar de knapsack , una lista de listas con el formato [id, benefit, weight]
    iterations : int 
        numero total de iteraciones (condicion de paro) para el algoritmo Iterative Local Search 
    hill_iterations : int 
        numero total de iteraciones (condicion de paro) para el algoritmo Hill Climbing 
    c : int 
        capacidad del ejemplar de knapsack 
    eta : float 
        fuerza de perturbacion para los metodos de perturbacion en Iterative Local Search 
    temp : int 
        temperatura para la condicion de aceptacion en el algoritmo Iterative Local Search
    repetitions : int 
        Total de repeticiones para obtener los datos para las pruebas de hipotesis, datos estadisticos y boxplots 
    w_one_path : string 
        la ruta del archivo para guardar la mejor solucion obtenida (usando ambos metodos de perturbacion) para el ejemplar 
    w_best_path : string 
        la ruta del archivo para guardar la muestra de los valores objetivos de las mejores soluciones encontradas ejecutando
        Iterative Local Search un numero total igual a repetitions 


    Returns: 

    Muestra una grafica de la evolucion promedio con ambos metodos de perturbacion. 
    ''' 
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

        print("{} Repetition COMPLETED".format(i))

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
    
    #Guardamos los mejores valores obtenidos en las 30 repeticiones 
    data_from_best_rand = [s.fitness_value for s in bests_rand]
    data_from_best_frec = [s.fitness_value for s in bests_frec]

    #Ahora tenemos que obtener al mejor, el promedio, el peor y la desviacion estandar de esas 30 iteraciones
    #Esto falta implementarse con pandas 

    #Encontramos a la mejor con RANDOM 
    best_random_sol = bests_rand[0]
    for sol in bests_rand:
        if sol.fitness_value <= best_random_sol.fitness_value:
            best_random_sol = sol 

    #Encontramos a la mejor con FRECUENCIAS 
    best_frec_sol = bests_frec[0]
    for sol in bests_frec:
        if sol.fitness_value <= best_frec_sol.fitness_value:
            best_frec_sol = sol     


    #Escribimos las mejores soluciones encontradas en ejecuciones individuales para el ejemplar recibido 
    kr.write_knapsack_file(w_one_path, ["Best Sol with Random Perturbation :\n",str(best_random_sol),"\nBest Sol with Frecuency Perturbation :\n", str(best_frec_sol)])

    #Guardamos el los arreglos con los mejores valores que seran usados para las pruebas de hipotesis 
    #y las graficas boxplot 
    kr.write_knapsack_file(w_best_path, [str(data_from_best_rand),"\n",str(data_from_best_frec)])        

    plt.title("Nombre : {} \nFuerza de Perturbacion : {}".format(instance_name,eta), loc = 'left')
    plt.xlabel("iterations")
    plt.ylabel("Fitness")
    plt.legend(['Random Perturbation', 'Frecuency Perturbation'])
    plt.plot(avr_evol_iter_total_r,avr_evol_fit_total_r,marker= 'o')
    plt.plot(avr_evol_iter_total_f,avr_evol_fit_total_f,marker= '*')
    
    plt.show()
    
def stadistic_data(sample_1,sample_2):
    '''
    Esta funcion recibe dos muestras e imprime los datos estadisticos de esas muestras 
    
    Args: 
    sammple_1 : list : list : int 
        Muestra del primer ejemplar 

    sammple_2 : list : list : int 
        Muestra del segundo ejemplar 

    '''
    df_r = pd.DataFrame({"Fitness Random" : sample_1})
    df_f = pd.DataFrame({"Fitness Frecuency " : sample_2})
    #print(df_r["Fitness"].std())
    print(df_r.describe())
    print(df_f.describe())

    pass 

def boxplot(sample_1,sample_2):
    '''
    Generacion de la grafica boxplot para las muestras 
    ''' 
    fig, ax = plt.subplots()
    bp = ax.boxplot([sample_1,sample_2],showfliers=False)
    plt.show()

    
def hypothesis_testing(sample_1,sample_2):
    '''
    Metodo que realiza las pruebas de hipotesis a partir de dos muestras 

    Args: 
    sammple_1 : list : list : int 
        Muestra del primer ejemplar 

    sammple_2 : list : list : int 
        Muestra del segundo ejemplar 
    
    Returns 
        1 : si la muestra 1 es la de mejor promedio 
        2 : si la muestra 2 es la de mejor promedio 
        -1 : si ambas muestras tienen la misma distribucion 
    '''

    #Comenzamos con la prueb de shapiro

    value  = 0.05

    if (stats.shapiro(sample_1).pvalue > value  and  stats.shapiro(sample_2).pvalue > value):
        #print("PASO SHAPIRO")
        #Pasamos el primer filtro, por lo que aplicamos Levene 
        stat, p = levene(sample_1, sample_2)
        if(p > value):
            #print("PASO LEVENE")
            #Entonces pasamos a ANOVA 
            if(f_oneway(sample_1,sample_2).pvalue > value):
                #print("PASO ANOVA") 
                #Entonces tienen la misma distribucion, por lo que no podemos concluir nada 
                return -1
            else : 
                return determine(sample_1,sample_2)
        else : #Usamos welch 
            #print("NO PASO LEVENE, PROCEDE A WELCH")
            if(stats.ttest_ind(random_sample ,frecuency_sample , equal_var = False).pvalue > value):
                #Entonces tienen la misma distribucion, por lo que no podemos concluir nada 
                return -1
            else : 
                return determine(sample_1,sample_2)

    else : #Si no cumple, realizamos la prueba de Kruskall -wells 
        #print("NO PASO SHAPIRO, PROCEDE A KRUSKALL")
        if (stats.kruskal(sample_1,sample_2).pvalue > value) :
            #Entonces tienen la misma distribucion, por lo que no podemos concluir nada 
            return -1 
        else : 
            #Determinamos quien tiene mayor promedio 
            return determine(sample_1,sample_2)
            

def comparation(n_comparations, sample_1, sample_2):

    #Contadores para ambos samples
    # Indice 0 para ejemplar 1 e indice 1 para ejemplar 2 
    conts = [0,0]
    for i in range(n_comparations):
        #Como hypothesis_testing regresa 0 o 1, aumentamos el contador respectivo 
        conts[hypothesis_testing(sample_1,sample_2)] = conts[hypothesis_testing(sample_1,sample_2)]+1 

    #A este punto ya guardamos cuantas veces fue bueno cada muestra correspondiente a los dos ejemplares 
    best = conts.index(max(conts)) # 0 : el mejor fue para la muestra 1, de lo contrario 1 : muestra 2 
    #Cuantas veces fue el mejor : 
    c_best = conts[best]
    c_worst = n_comparations - c_best

    #Regresamos [mejor estrategia segun las pruebas de hipotesis, proporcion en que esa estrategia fue mejor, proporcion en que la estrategia fue peor]
    return best, 100*c_best/n_comparations, 100*c_worst/n_comparations
    #Necesitamos regresar en que proporcion fue el mejor, por lo que el total es n_comparations


def determine(sample_1, sample_2):

    '''
    Funcion auxiliar que recibe dos arreglos, tipicamente las muestras de los mejores resultados 
    obtenidos en las 30 repeticiones y se utiliza para determinar el algoritmo de mejor rendimiento 
    basándonos en aquel con menor promedio (recordemos que la funcion objetivo busca minimizar)

    Args: 
    sample_1 : list : int 
    sample_2 : list : int 
        Las muestras de los mejores resultados 
    Returs: 
        0, 1 : 0 si sample_1 tiene el menor promedio, en otro caso regresa 1  

    '''
    mean_1 = sum(sample_1)/len(sample_1)
    mean_2 = sum(sample_2)/len(sample_2)

    #Como nuestra funcion de evaluacion es de minimizacion, entonces debemos considerar el de menor promedio 
    if min(mean_1,mean_2) == mean_1 :
            return 0 
    else : 
            return 1 



if __name__ == '__main__': 
    '''
    Funcion main, en donde se realiza la lectura y escritura de archivos asi como la ejecucion del algoritmo ILS 

    '''
    

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


    s_best, fitnestt_d, iter_d, avg_evol = ils.iterative_local_search(data,iterations,hill_iterations,c,0,eta,20)
    print(s_best)
    #s_best_1, fitnestt_d_1, iter_d_1, avg_evol_1 = ils.iterative_local_search(data,iterations,hill_iterations,c,1,eta,20)
    

    #draw_graph_pertubations_comparations(w_paths_one_sol, eta, [iter_d,fitnestt_d], [iter_d_1,fitnestt_d_1],n,[s_best.fitness_value,s_best_1.fitness_value])


    #Para evolucion promedio : 
    #generate_avg_evol(data,iterations,hill_iterations,c,eta,20,10, w_paths_one_sol, w_paths_best_sols,paths[int(sys.argv[1])])


    #Se leen los mejores resultados depues de ejecutar ITS 10 veces 
    #samples = kr.read_sample_data(w_paths_best_sols)
    #Se almacenan las muestras de esas 10 veces 
    #random_sample = samples[0]
    #frecuency_sample = samples[1]

    #Datos estadisticos : 
    #stadistic_data(random_sample,frecuency_sample)

    #Para mostrar la grafica de boxplot : 
    #boxplot(random_sample,frecuency_sample)


    #Para obtener los resultados de las pruebas de hipotesis : 
    #best, b_p, w_p = comparation(10,random_sample,frecuency_sample)
    
    