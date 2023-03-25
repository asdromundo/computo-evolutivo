import knapsack as kp 


def hill_climbing(solution, iterations, capacity):
	'''
	Implementacion del algoritmo Hill Climbing

	Args: 
	solution : Solution 
		Solucion recibida 
	iterations : int 
		Condicion de paro : numero de iteraciones 
	capacity : int 
		Capacidad maxima 

	'''
	current_sol = solution
	for i in range(iterations):
		
		best_neighbor = kp.neighborhood_operator(current_sol, capacity,7)
		if best_neighbor.fitness_value > current_sol.fitness_value:
			#Entonces ya no se puede mejorar 
			break 
		else:
			current_sol = best_neighbor


	return current_sol 	


