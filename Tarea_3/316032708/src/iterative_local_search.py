import math  
import random as rnd  
from copy import deepcopy
import numpy as np

import knapsack as kp 
import hill_climbing as hc 


def iterative_local_search(data,iterations,hill_iterations,capacity,mode,eta,t):
	'''
	Implementacion de busqueda local iterativa 

	Args: 
	data : list : list : [id : int, beneficio : int, peso : int]
		Es el conjunto total de items pertenecientes al ejemplar 
	iterations : int 
		Condicion de paro, numero de iteraciones *NOTA EN REPORTE 
	capacity : int 
		Capacidad maxima del ejemplar 
	mode : int 
		Es una bandera para determinar qu\'e metodo de perturbacion utilizar 
	eta : float 
		Es la fuerza de perturbacion 
	t : int 
		temperatura 
	Returns: 
	s_best : Solution 
		La mejor solucion encontrada 
	'''	
	#Generamos la solucion iniicial de forma aleatoria 
	first_sol = kp.generate_random_sol(data)
	#Primera solucion con optimizacion local 
	s_hc = hc.hill_climbing(first_sol, hill_iterations, capacity)

	s_best = s_hc
	#Historial para la perturbacion por frecuencia 
	record = []

	#Listas para visualizacion
	iter_data = np.array([0 for i in range(iterations)])
	fitness_data = np.array([0 for i in range(iterations)])

	#Datos para evolucion promedio
	#Cada iteraciones/n veces guardamos el valor 
	n_sections = .05
	section = n_sections
	average_iter = 0 
	average_evolution = []

	#Temperatura inicial 
	temperature = t 

	if(mode > 1 or mode < 0):
		mode = 1

	#Historial para la perturbacion por frecuencia 
	record = [0 for i in range(len(first_sol.carried_items)+ len(first_sol.no_carried_items))]

	s_p = None 
	for i in range(iterations):
		if mode == 1: 
			s_p = frecuency_perturbation(s_best,record,eta)
		else : 
			s_p = random_perturbation(s_best,eta)
		
		s_hc_p = hc.hill_climbing(s_p,hill_iterations,capacity)

		if s_hc_p.fitness_value <= s_best.fitness_value:
				
				s_best = s_hc_p		
		elif  prob(s_best,s_hc_p,t) < rnd.uniform(0,1):
				
				s_best = s_hc_p

		t = slow_cooling_schema(t,0.05)

		#Guardamos los datos 
		iter_data[i] = i 
		fitness_data[i] = s_best.fitness_value	
		
		#Cada iteraciones/part vamos a recabar la mejor solucion 
		if i == int(iterations*n_sections):
			average_iter = average_iter+1
			n_sections = n_sections+section
			average_evolution.append([average_iter, s_best.fitness_value])
			

	#Tenemos que regresar tambien un arreglo de tuplas [(iteracion, mejor_resultado)]
	return s_best, fitness_data, iter_data, average_evolution 

def prob(current_sol,next_sol,temperature):
    '''
	Probabilidad de aceptacion dada una solucion vecina de la solucion actual 
	Args:
	next_sol : list : list : [id : int, beneficio : int, peso : int]
		solucion candidata a ser solucion actual 
	Returns 
        proba : float 
		proabilidad de ser aceptada  
	'''    
    return math.pow( math.e, - (( next_sol.fitness_value - current_sol.fitness_value)/temperature)) 

def slow_cooling_schema(temperature,cooling_beta):
	'''
	Esquema de enfriamiento con decremento lento. Cada iteracion disminuye la temperatura usando el valor de cooling_beta 
	'''
	# T = T / (1 + betha * T)
	# betha : 0.001, 0.005, 0.01
	return temperature / 1+ cooling_beta*temperature

def random_perturbation(best_sol, strong):
	'''
	Estrategia de perturbacion basada en seleccionar indices de elementos de Solution.carried_items de forma aleatoria 
	
	Args: 
	best_sol : Solution
		Solucion a perturbar  
	strong : float 
		Fuerza de perturbacion para determinar a cuantos elmentos de la solucion se va a perturbar

	Returns: 
	perturbed_sol : Solution

	'''
	# Obtenemos el numero de elementos a ser perturbados (estos elementos van a ser perturbados en carried_items) 
	eta = math.floor(len(best_sol.carried_items)*strong)

	#Obtenemos una muestra aleatoria de carried_items 
	random_items = rnd.sample(best_sol.carried_items, eta)
	#Obtenemos los indices 
	indices = [best_sol.carried_items.index(e) for e in random_items]

	p_solution = deepcopy(best_sol)

	#Perturbamos la solucion 
	new_carried, new_no_carried =[],[]


	#Perturbamos la solucion 
	if(len(indices) > len(p_solution.no_carried_items)):
		indices = indices[:len(p_solution.no_carried_items)]

	new_carried, new_no_carried = many_swaps(p_solution.carried_items, p_solution.no_carried_items, indices)	

	
	return kp.Solution(new_carried, new_no_carried) 

def frecuency_perturbation(best_sol, record, strong):
	'''
	Estrategia de perturbacion basada en un arreglo de frecuencias "record"

	Args: 
	best_sol : Solution
		Solucion a perturbar  
	record : list [int]
		Historial de perturbaciones, en este caso es el arreglo de frecuecnias 
	strong : float 
		Fuerza de perturbacion para determinar a cuantos elmentos de la solucion se va a perturbar 


	Returns : 
	perturbed_sol : Solution 
	'''

	# Obtenemos el numero de elementos a ser perturbados (estos elementos van a ser perturbados en carried_items) 
	eta = math.floor(len(best_sol.carried_items)*strong)

	# Obtenemos el indice de los primeros "eta" elementos de nuestro historial "record" que tienen menor valor
	# Es decir obtenemos los elementos con menor frecuencia para ser perturbados 
	indices = find_smallest_indices(record[:len(best_sol.carried_items)], eta)

	
	p_solution = deepcopy(best_sol)

	new_carried, new_no_carried =[],[]


	#Perturbamos la solucion 
	if(len(indices) > len(p_solution.no_carried_items)):
		indices = indices[:len(p_solution.no_carried_items)]

	new_carried, new_no_carried = many_swaps(p_solution.carried_items, p_solution.no_carried_items, indices)	

	for index in indices:
			record[index] = record[index]+1

	return kp.Solution(new_carried, new_no_carried) 

def find_smallest_indices(record, k):
	'''
	Funcion que recibe el arreglo de frecuencias y un entero k, regresa los 
	k indices de los elementos con menor frecuencia. 

	Args : 
	record : list [int]
		arreglo de frecuencias F
	k : int 

	Returns : 
	indices : list[int]
		Arreglo con los índices en el arreglo de frecuencias con menor valor 
	'''

	#Se ordena en orden ascendente la lista de frecuencias y se consideran los k menores elementos  
	minor_frecuency = sorted(record)[:k]

	#Encontramos los indices con menor frecuencia 
	indices = [i for i,x in enumerate(record) if x in minor_frecuency]

	return indices

def many_swaps(list_one, list_two, indices):

	#Es importante verificar que ambas listas tengan al menos la cantidad de indices 
	#En general la lista dos es la que tendrá menos elemetos 
	#Vamos a considerar a los primeros list_two[len(indices)]

	#Tenemos que basarnos en la maxima cantidad de elementos en list_two 
	#primero revisamos 

	#Obtenemos los elemento de la primer lista 
	temp_elements_1 = [list_one[index] for index in indices]

	#Obtenemos los elementos de la segunda lista de forma aleatoria
	temp_elements_2 = rnd.sample(list_two, len(indices))

	#Removemos los elementos
	for e in temp_elements_1 : 
		list_one.remove(e)

	for e in temp_elements_2 : 
		list_two.remove(e)	

	return list_one + temp_elements_2, list_two + temp_elements_1

