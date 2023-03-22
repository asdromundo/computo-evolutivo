import random as rnd 
from copy import deepcopy

class Solution: 
	'''
	Clase que modela una solucion para el problema de 0-1 knapsack 


	Attributes 
	----------
	carried_items : list : [id : int, beneficio : int, peso : int]
		lista de items que considerados para beneficio y peso 
	no_carried_items :  list : [id : int, beneficio : int, peso : int]
		lista de items que no son considerados pero que forman parte del conjunto general de items 

	'''


	def __init__(self,carried_i, no_carried): 
		'''
		Constructor 
		'''
		self.carried_items = carried_i
		self.no_carried_items = no_carried

	def __str__(self):
		return "Loaded Items: "+ str(self.carried_items) + "\n" +"Non Loaded Items: "+ str(self.no_carried_items)+ "\n" + "Total Benefit :"+str(self.get_value()) + "\n" + "Total Weight :"+ str(self.get_weight())


	def get_weight(self):
		return sum(item[2] for item in self.carried_items)


	def get_value(self):
		return sum(item[1] for item in self.carried_items)		


def generate_random_sol(data) : 

	carried_items= []
	no_carried_items = []

	for i in range(len(data)):

		if rnd.uniform(0,1) < .5 : 	
			carried_items.append(data[i])
		else : 
			no_carried_items.append(data[i])


	return Solution(carried_items, no_carried_items)

def neighborOperator(solution, capacity):
	'''
	Args: 
	solution : Solution 
		La solucion a la cual encontrar el vecino   
	capacity : int 
		La capacidad que no podemos exceder 

	Returns: 
	neighbor : Solution 
		Una solucion vecina 


	Funcion que recibe una instancia de la clase Solution y regresa un vecino de esa clase 
	
	Hay tres posibles opciones : 
	- Quitar 2 elemenots de carried_items y agregar 1 elemento de no_carried_items
	- Quitar 1 elemento de carried_items y agregar 2 elementos de no_carried_items
	- Intercambiar 2 items de carried_items con 2 items de  no_carried_items

	'''

	#Hacemos una copia de la solucion
	neighbor = Solution(solution.carried_items, solution.no_carried_items)


	#OPCION 1 :
	neighbor_1 = deepcopy(neighbor) 
	#2 Elementos de carried_items : 
	deleted_items = rnd.sample(neighbor.carried_items, k=2)
	#1 Elemento de no_carried_items : 
	new_item = rnd.choice(neighbor.no_carried_items)
	
	#Eliminamos los elementos de carried_items  
	neighbor_1.carried_items.remove(deleted_items[0])
	neighbor_1.carried_items.remove(deleted_items[1])
	#Agregamos el elemnto 
	neighbor_1.carried_items.append(new_item)


	neighbor_1.no_carried_items.remove(new_item)
	neighbor_1.no_carried_items.append(deleted_items[0])
	neighbor_1.no_carried_items.append(deleted_items[1])
 

	if neighbor_1.get_weight() <= capacity : 
		return neighbor_1


	#OPCION 2 : 
	neighbor_2 = deepcopy(neighbor)
	#1 Elemento de carried_items : 
	deleted_item = rnd.choice(neighbor.carried_items)
	#2 Elementos de no_carried_items : 
	new_items = rnd.sample(neighbor.no_carried_items, k=2)
	
	#Eliminamos los elementos de carried_items  
	neighbor_2.carried_items.remove(deleted_item)
	#Agregamos el elemnto 
	neighbor_2.carried_items.append(new_items[0])
	neighbor_2.carried_items.append(new_items[1])

	neighbor_2.no_carried_items.remove(new_items[0])
	neighbor_2.no_carried_items.remove(new_items[1])
	neighbor_2.no_carried_items.append(deleted_items)

	if neighbor_2.get_weight() <= capacity : 
		return neighbor_2



	#OPCION 3 : 
	neighbor_3 = deepcopy(neighbor)
	#2 Elementos de carried_items : 
	deleted_items = rnd.sample(neighbor.carried_items,k=2)
	#2 Elementos de no_carried_items : 
	new_items = rnd.sample(neighbor.no_carried_items, k=2)

	#Eliminamos los elementos de carried_items 
	neighbor_3.carried_items.remove(deleted_items[0])
	neighbor_3.carried_items.remove(deleted_items[1])
	#Agregamos los elemenots 
	neighbor_3.carried_items.append(new_items[0])
	neighbor_3.carried_items.append(new_items[1])

	neighbor_3.no_carried_items.remove(new_items[0])
	neighbor_3.no_carried_items.remove(new_items[1])

	neighbor_3.no_carried_items.append(deleted_items[0])
	neighbor_3.no_carried_items.remove(deleted_items[1])

	if neighbor_3.get_weight() <= capacity : 
		return neighbor_3


	#Si ninguno de los casos resulta ser una solucion valida, regresamos la misma solucion
	return neighbor










