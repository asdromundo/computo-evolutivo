import knapsack as kp 


def hill_climbing(solution, iterations, capacity):
	'''
	Implementacion del algoritmo Hill Climbing

	'''
	current_sol = solution
	for i in range(iterations):
		
		best_neighbor = kp.neighborhood_operator(current_sol, capacity,7)

