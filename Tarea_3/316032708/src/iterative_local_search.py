import math  
import random as rnd  
from copy import deepcopy

import knapsack as kp 
import hill_climbing as hc 


def iterative_local_search(data,iterations,capacity):
	
	first_sol = kp.generate_random_sol(data)
	s_hc = hc.hill_climbing(first_sol, 3000, capacity)

	s_best = s_hc
	
	record = record = [0 for i in range(len(first_sol.carried_items)+ len(first_sol.no_carried_items))]

	for i in range(iterations):
		s_p = frecuency_perturbation(s_best,record,.5)
		s_hc_p = hc.hill_climbing(s_p,3000,capacity)

		if s_hc_p.fitness_value < s_best.fitness_value:
			s_best = s_hc_p

	print(record)
	return s_best 

def frecuency_perturbation(best_sol, record, strong):
	'''
	Estrategia de perturbacion 

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

	#Perturbamos la solucion 
	p_solution = deepcopy(best_sol)

	new_carried, new_no_carried =[],[]

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
	#Aqui no hemos considerado que pasa si la lista de items que no son cargados no tiene suficientes elementos 
	temp_elements_2 = rnd.sample(list_two, len(indices))

	#Removemos los elementos
	for e in temp_elements_1 : 
		list_one.remove(e)

	for e in temp_elements_2 : 
		list_two.remove(e)	

	return list_one + temp_elements_2, list_two + temp_elements_1

