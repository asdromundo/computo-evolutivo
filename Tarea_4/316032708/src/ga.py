
import math 
import numpy as np 
import random as rnd 
import copy

import queen_rep as qrep 

class GeneticAlg: 
	'''
	Class modeling the steps and operators of a genetic algorithm to resolve the n-queens problem 

	Attributes : 
	queens : int 
		Number of the n-queen problem
	pop_size : int 
		Size of the population 
	sel_prob : float  //Esto aun no se determina por que todos los individuos tienen la misma proba de ser seleccionados
		Probability of select a individual from the population 
	cross_prob : float 
		Probability of crossover  
	mut_prob : float 
		Probability of select a individual from the population in order to be mutated 



	'''



	'''
	Él proseso es : 
	Inicializamos nuestra poblacion (de forma aleatoria) de tamaño N

	Vamos a determinar cuantos vamos a seleccionar por metodo de ruleta y cuantos por elitismo
	Si vamos a realizar K selecciones, entonces vamos a elegir N-K individuos de forma aleatoria 
	
	A esos K seleccionados les vamos a aplicar cruza , entonces tenemos que hacer parejas y a esas parejas 
	usamos la probabilidad de cruza para determinar si se cruzan o no, si no se cruzan entonces los regresamos como estaban
	Por lo que obtenemos K_1 individuos de la siguiente generacion 

	A esos K_1 individuos les vamos intentar aplicar mutacion 

	'''

	def __init__(self, n_q, pop_s, p_sel,cross_p, mut_p):

		self.n_queens = n_q 
		self.pop_size = pop_s
		self.current_pop = []
		self.sel_proportion = p_sel
		self.cross_prob = cross_p
		self.mut_prob = mut_p

	def show_pop(self):
		for ind in self.current_pop:
			print(ind)

	def init_population(self):
		'''
		Generate the initial population and asigns to the current population 
		Each individual is a permutation from the numbers 0 to n_queens (exclusive)
		'''
		init_pop = []

		for i in range(self.pop_size):
			init_pop.append(qrep.Queen_Solution(np.random.permutation(self.n_queens)))


		self.current_pop=init_pop
		[ind.evaluate() for ind in self.current_pop]


	#Para la seleccion por ruleta 
	# muestra = random.choices(lista, weights=[lista de probabilidades para lista], k = tamanio de la muestra )
	def selection_rl(self):
		'''
		Selection  by Roulette

		Returns : 
		select_pop : list : Queen_Solution
			The selected individuals to be parents 
		'''

		#Evaluate each individual
		[ind.evaluate() for ind in self.current_pop]
		#The total sum of fitness
		fit_sum = sum([ind.fitness for ind in self.current_pop])
		#Generate the probabilities array
		probs = [ind.fitness/fit_sum for ind in self.current_pop]

		#Selection by roulette
		return rnd.choices(self.current_pop, weights=probs, k=int(self.pop_size*self.sel_proportion))

	def selection_elitism(self):

		[ind.evaluate() for ind in self.current_pop]
		return sorted(self.current_pop, key = lambda solution : -solution.fitness)[:self.pop_size-int(self.pop_size*self.sel_proportion)]		


	def crossover(self, p_1, p_2):
		'''
		Crossover operator for permutations  

		p1 : Queen_Solution
			first parent
		p2 : Queen_Solution
			second parent 

		Returns: 

		s_1 : Queen_Solution
			first son 
		s_2 : Queen_Solution
			second son 
		'''
		if (rnd.random() < self.cross_prob):
			#The crossover happends
			#First we generate the two points of crossover 
			cross_p_1 = math.floor(self.n_queens/4)
			cross_p_2 = math.floor(3*(self.n_queens/4))

			ra = range(self.n_queens)

			#Initialize the son's chromosomes
			son_1_chromosome = [-1 for x in ra]
			son_2_chromosome = [-1 for x in ra]

			#Set the first parents information 
			son_1_chromosome[cross_p_1:cross_p_2] = p_2.chromosome[cross_p_1:cross_p_2]
			son_2_chromosome[cross_p_1:cross_p_2] = p_1.chromosome[cross_p_1:cross_p_2]

			cont_select = cross_p_2
			cont_insert = cross_p_2

			while(-1 in son_1_chromosome):
				if p_1.chromosome[cont_select%self.n_queens] not in son_1_chromosome:
					son_1_chromosome[cont_insert%self.n_queens] = p_1.chromosome[cont_select%self.n_queens]
					cont_select = cont_select+1 
					cont_insert = cont_insert+1 
				else : 
					cont_select = cont_select+1 

			cont_select = cross_p_2
			cont_insert = cross_p_2

			while(-1 in son_2_chromosome):
				if p_2.chromosome[cont_select%self.n_queens] not in son_2_chromosome:
					son_2_chromosome[cont_insert%self.n_queens] = p_2.chromosome[cont_select%self.n_queens]
					cont_select = cont_select+1 
					cont_insert = cont_insert+1 
				else : 
					cont_select = cont_select+1 


			return qrep.Queen_Solution(np.array(son_1_chromosome)),qrep.Queen_Solution(np.array(son_2_chromosome)) 		

		else:
			return copy.deepcopy(p_1), copy.deepcopy(p_2)


	def mutate_individual(self,individual):

		index_1, index_2 = rnd.sample(range(len(individual.chromosome)), 2)
		individual.chromosome[index_1], individual.chromosome[index_2] = individual.chromosome[index_2],individual.chromosome[index_1] 



	def mutation_simple(self):
		'''
		Mutation operator, for each individual check if the probability of mutation is less than a random 
		float, if is then it swaps two random index of the individual chromosome 

		'''
		#for sol in self.current_pop:


		pass

if __name__ == '__main__':

	ga = GeneticAlg(20,10,.7,.8,.1)
	ga.init_population()
	for ind in ga.current_pop: 
		print(ind)
	print(">>>>>>>>>>>>")
	thebest = ga.selection_elitism()
	for ind in thebest:
		print(ind)
	
	print(">>>>>>>>>>>>>>>>MUTATION")
	print(ga.current_pop[0])
	print(">>>>>>>>>>>>>>>>>.MUTADO")
	ind = ga.current_pop[0]
	#len(ind)
	ga.mutate_individual(ind)
	ind.evaluate()
	print(ind)
	#ga.mutate_individual(ga.current_pop[0])


	#print("Parents >>>>>>>>>>>>>>>>>>>>>")
	#print(ga.current_pop[0])
	#print(ga.current_pop[1])

	#print("Sons >>>>>>>>>>>>>>>>>>>>>")
	#son1, son2 = ga.crossover(ga.current_pop[0],ga.current_pop[1]) 
	#print(son1)
	#print(son2)	



	




