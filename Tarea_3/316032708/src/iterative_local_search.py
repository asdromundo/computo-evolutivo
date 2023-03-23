import knapsack as kp 
import hill_climbing as hc 


def iterative_local_search():
	pass


def perturbation(best_sol, record):
	'''
	Estrategia de perturbacion 

	Args: 
	best_sol : Solution 
	record : list [int]

	Returns : 
	perturbed_sol : Solution 
	'''
	# El arreglo va a ser del tipo [1,0,0,2,....] mostrando la frecuencia con que fue perturbado 
	#Primero tenemos que revisar 



	#Necesitamos un arreglo que lleve registros sobre qué indices  de la Solution.carried_items fueron perturbados 
	#La cuestion es que el operador de vecindad agrega Y swapea elementos SOLO cuando la capacidad ha sido excedida 
	#Entonces, la solucion que recibimos debe ya tener un tamanio fijo (en teoria) por lo que el arreglo de frecuencias F
	#El cual va a ser del mismo tamanio que Solution.carried_items, entonces es posible que en alguna iteracion se cambien 
	#El tamanio de la solucion 
	
	#Aqui el pedo es que el arreglo de frecuencias debe ser del mismo tamanio 
	pass

def get_frecuency_array(sol, record):

	#Puede ser que el arreglo sea del tamanio de todos los items pero en ese caso, como vamos a considerar 
	#A los primeros elementos menores de un arreglo ? 

	#Hay que revisar si len(sol.carried_items) == len(record)

	#Si  len(sol.carried_items) < len(record)
	#Entonces hay que elminar el ultimo registro de record por que 


	pass 



def find_smallest_indices(record, k):
	'''
	Funcion que recibe el arreglo de frecuencias y un entero k, regresa los 
	k indices de los elementos en frecuencias con menor frecuencia. 

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
