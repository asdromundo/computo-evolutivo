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
		self.max_value = sum(item[1] for item in self.carried_items) + sum(item[1] for item in self.no_carried_items)
		self.fitness_value = self.max_value-sum(item[1] for item in self.carried_items) 
		self.total_items = len(self.carried_items) + len(self.no_carried_items)

	def __str__(self):#+"Fitness value: "+str(self.fitness_value)
		return "Loaded Items: "+ str(self.carried_items) + "\n" +"Non Loaded Items: "+ str(self.no_carried_items)+ "\n" + "Total Benefit :"+str(self.get_value()) + "\n" + "Total Weight :"+ str(self.get_weight()) + "\n" +"Fitness Min:"+ str(self.fitness_value) + "\n" +"Fitness Max:"+ str(self.max_value-self.fitness_value) 

	def get_weight(self):
		return sum(item[2] for item in self.carried_items)


	def get_value(self):
		return sum(item[1] for item in self.carried_items)		


def generate_random_sol(data) : 
	'''
	Funcion para generar una soluciion aleatoria 

	Args: 
	data : list : [id : int, beneficio : int, peso : int]
		El total de items a considerar para generar la solucion 

	Returns: 
	solution : Solution 
		Una solucion que considera items con una probabilidad de .5 

	'''
	carried_items= []
	no_carried_items = []

	for i in range(len(data)):

		if rnd.uniform(0,1) < .6 : 	
			carried_items.append(data[i])
		else : 
			no_carried_items.append(data[i])


	return Solution(carried_items, no_carried_items)

def evaluate(solution):
	'''
	Funcion para obtener el valor objetivo de una solucion, funciona restando la suma total del beneficio 
	de los items que la solucion carga menos el beneficio maximo que se obtiene al sumar el beneficio de 
	cada item del conjunto total. 

	Args: 
	solution : Solution 
		Solucion a evaluar 

	max_benefit: int 
		Maximo beneficio obtenido al sumar todos los items del conjunto total 
	'''
	return solution.max_value - solution.get_value()


def neighbor_operator(sol,capacity):

	'''
	Operador de vecindad 
	
	Args:
	sol : Solution 
		Solucion a la que encontrar el vecino 
	capacity : int 
		Capacidad maxima del problema 0-1 knapsack

	Returns : 
	neighbor : Solution 
		Solucion vecina valida  

	'''
	neighbor = Solution(sol.carried_items,sol.no_carried_items)

	temp_item_1 = rnd.choice(neighbor.carried_items)
	#Si ya no hay elementos que considerar se regresa la solucion 
	if(neighbor.no_carried_items == []):
		return neighbor
	temp_item_2 = rnd.choice(neighbor.no_carried_items)


	if neighbor.get_weight() < capacity : 
		neighbor.carried_items.append(temp_item_2)
		neighbor.no_carried_items.remove(temp_item_2)
	else :
		#Encontramos al item de menor peso del conjunto que no carga 
		#sort_nc = sorted(neighbor.no_carried_items,key=lambda x: x[2])
		#temp_item_2 = sort_nc[0] 
		#Encontramos al item de mayor peso del conjunto que carga 
		#sort_c = sorted(neighbor.carried_items,key=lambda x: x[2])	
		#temp_item_1 = sort_c[-1]
		#Para mejorar esto podemos asignarle a cada item un valor de aptitud 

		neighbor.carried_items.remove(temp_item_1)
		neighbor.no_carried_items.remove(temp_item_2)

		neighbor.carried_items.append(temp_item_2)
		neighbor.no_carried_items.append(temp_item_1)

	return neighbor

def neighborhood_operator(solution, capacity,epsilon):
	'''

	'''

	neighborhood = []
	
	#Generamos una vecindad de tamanio epislon 
	for i in range(epsilon):
		neighborhood.append(neighbor_operator(solution, capacity))
		

	#Obtenemos al mejor vecino 
	best_neighbor = neighborhood[0]
	for neighbor in neighborhood :
		#Buscamos minimizar  
		if neighbor.fitness_value <= best_neighbor.fitness_value:
			best_neighbor = neighbor


	return best_neighbor  


def best_of_all_neighbor(solution,capacity):
	'''
	Funcion para considerar al mejor vecino dado una vecindad 

	Args: 
	solution : Solution 
		Solucion que evaluar 

	Returns : 
	best_neighbor : Solution 
		Mejor vecino de la vecindad 
	'''

	neighborhood = []

	if(solution.get_weight() < capacity):
		#Esta lista es AGREGANDO items ya que la capacidad no ha sido excedida
		for item in solution.no_carried_items:
			tem_sc = solution.carried_items+[item]
			temp_snc = [it for it in solution.no_carried_items if it != item] 
			neighborhood.append(Solution(tem_sc, temp_snc))
	else : 
		#Si no, entonces hay que swapear un elemento random de la solucion 
		#Obtenemos el elemento a swapear en la funcion 
		swap_item = rnd.choice(solution.carried_items)
		#Generamos la vecindad cambiando ese elemento 
		for item in solution.no_carried_items:
			tem_sc = [it for it in solution.carried_items+[item] if it != swap_item]

			temp_snc = [it for it in solution.no_carried_items+[swap_item] if it != item]

			neighborhood.append(Solution(tem_sc, temp_snc))


	best_sol = neighborhood[0] 

	for neighbor in neighborhood:
		if neighbor.fitness_value < best_sol.fitness_value : 
			best_sol = neighbor

	return neighbor






