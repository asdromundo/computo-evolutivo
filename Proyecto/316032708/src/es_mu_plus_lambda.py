import functions 
import numpy as np
import random as rnd 
import es_individual as ind 
import matplotlib.pyplot as plt
import time as tm 
class ESMuPlusLambda: 
	'''
	Implementation of the Evolutionary Strategy Mu + Lambda 

	Attributtes: 

	funtion : fun : R^n -> R 
		funtion to optimize 
	
	func_range = (float , float)
		The domain of the funtion 

	mu : int 
		Size of population 

	lamb(lambda) : int 
		Size of offspring 

	rho : int 
		Mix number 

	m : checker 
		iterations threshold to the self-adaptation step 

	dim : int 
		Dimention of the solutions 

	'''



	def __init__(self, fun, fun_rg, mu, lam, rho, m,dim):
		self.function = fun
		self.func_range = fun_rg
		self.mu = mu	
		self.lamb = lam 
		self.rho = rho
		self.m = m 
		self.dim = dim 
		self.sigma = rnd.uniform(0.1, 2.0)
		self.iters = 0  #Iterations counter 
		self.sucess = 0  #Succes counter
		self.c = 0.817 #Change Factor 
		self.current_p = [] #Current population initialized as empty

	def __str__(self):
		return "Mu value : {}".format(str(self.mu))+"\n"+"Lambda value : {}".format(str(self.lamb))+"Dominion Dimention : {}".format(self.dim)

	def print_current_pop(self,pop):
		for ind in pop: 
			print(ind)

	def evaluate_pop(self, population):
		for ind in population:
			ind.evaluate()

	def random_pop_generator(self):
		'''
		It generate a random population based on mu individuals and based on the dimension and range of the funtion 
		'''
		vectors = np.array([np.array([np.random.uniform(self.func_range[0], self.func_range[1]) for i in range(self.dim)]) for j in range(self.mu)])
		population = np.array([ind.ESIndividual(vector,self.sigma, self.function, self.func_range) for vector in vectors])
		#return population 
		self.evaluate_pop(population)
		self.current_p = population 

	def parents_selection(self): 
		return np.random.choice(self.current_p,size=self.rho, replace=False)

	#RECOMBINATIONS 
	def discrete_recombination(self, parents): 

		#We extract the vectors from the parents 
		vector_matrix = np.array([parent.vector for parent in parents])

		#We extract the sigmas from the parents 
		sigmas = np.array([parent.sigma for parent in parents])


		genotype = []
		for i in range(self.dim):
			new_gen = np.random.choice(np.take(vector_matrix,i,axis=1), 1, replace=False)[0] 
			genotype.append(new_gen)
		
		#Chose one sigma randomly 
		new_sigma = np.random.choice(sigmas,1,replace=False)[0]

		child = ind.ESIndividual(np.array(genotype),new_sigma,self.function,self.func_range) 
		child.evaluate()

		return child

	def  intermediate_recombination(self,parents):

		#We extract the vectors from the parents 
		vector_matrix = np.array([parent.vector for parent in parents])

		#We extract the sigmas from the parents 
		sigmas = np.array([parent.sigma for parent in parents])

		#genotype =[]

		genotype = [((sum(np.take(vector_matrix,i,axis=1)))/self.dim) for i in range(self.dim)]

		new_sigma = sum(sigmas)/len(sigmas)

		child = ind.ESIndividual(np.array(genotype),new_sigma,self.function,self.func_range)
		child.evaluate()

		return child 

	def discrete_offspring(self):
		offspring =[]
		for i in range(self.lamb):
			# Select the parents 
			parents = self.parents_selection()
			# Recombination 
			offspring.append(self.discrete_recombination(parents))
		return np.array(offspring)


	def intermediate_offspring(self):
		offspring =[]
		for i in range(self.lamb):
			# Select the parents 
			parents = self.parents_selection()
			# Recombination 
			offspring.append(self.intermediate_recombination(parents))
		return np.array(offspring)		

	def mutate(self, individual):

		#Generate a random number using normal distribution 
		r = np.random.normal(0,individual.sigma*individual.sigma,len(individual.vector))
		new_ind = ind.ESIndividual(individual.vector+r,individual.sigma,self.function,self.func_range) 
		#We fix the vector in case that some value has passed the function range dominion 
		new_ind.fix_genotype()

		new_ind.evaluate()

		return new_ind  
	
	
	def mu_plus_lambda_selection(self, offspring):

		selection_pool = np.append(self.current_p, offspring)
		
		#We select the best mu individuals from the selection pool 
		self.current_p = sorted(selection_pool, key = lambda individual : individual.fitness)[:self.mu]


	def get_the_best(self):
		return sorted(self.current_p, key = lambda individual : individual.fitness)[0] 

	def execute(self, max_iterations,recombination):
		
		start = tm.time()
		#Generate the initial population (radom)
		self.random_pop_generator()
		
		iterations_info = []
		best_fitness_info = []
		sigma_evolution = []
		#Max generations 
		for j in range(max_iterations):
			#Select the parents 
			parents = self.parents_selection()
			
			
			#Recombination 
			#Discrete 
			if(recombination == 0):
				offspring = self.discrete_offspring()
			else :
				offspring = self.intermediate_offspring() 
			#Intermediate 
			#Mutate 
			for i in range(len(offspring)): 
				ind_mut = self.mutate(offspring[i])

				#If the mutated solution is better than the original 
				if ind_mut.fitness < offspring[i].fitness:
					offspring[i] = ind_mut  
					offspring[i].evaluate()
					self.sucess = self.sucess	+1 
			#Self Adaptation Step 
			
			if self.iters == self.m :
				#If we have reached the iteratiosn threshold
				for ind in offspring:
					if self.sucess/self.m < 1/5 :
						ind.increase_sigma(self.c)
					if self.sucess/self.m > 1/5 :
						ind.decrease_sigma(self.c)
				self.iters = 0 
				self.sucess = 0

			
			#Mu + Lambda selection 
			self.mu_plus_lambda_selection(offspring)
			#print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			#self.print_current_pop(self.current_p)

			self.iters = self.iters + 1 


			iterations_info.append(j)
			sigma_evolution.append(self.get_the_best().sigma)
			best_fitness_info.append(self.get_the_best().fitness)

		end = tm.time()
		total_time = end-start

		return self.get_the_best(),np.array(iterations_info),np.array(best_fitness_info), np.array(sigma_evolution), total_time 


	#Tenemos que realizar la ejecucion promedio 

def execute_single(max_iterations, recombination): 

	the_best, ind_iters, ind_fit, ind_sig, time =  ESMuPlusLambda(functions.ackley,(-30,30), 20, 100, 10, 10,2).execute(max_iterations,recombination)

	return the_best, ind_iters, ind_fit, ind_sig, time

def execute_repetitve(repetitions, max_iterations, recombination): 

	rep_iterations = []
	rep_fitness = []
	rep_best = []
	rep_sigmas = []
	times = []

	for i in range(repetitions):
		temp_best, temp_iters, temp_fit, sigmas, t = ESMuPlusLambda(functions.ackley,(-30,30), 20, 100, 10, 10,2).execute(max_iterations,recombination)

		rep_iterations.append(temp_iters)
		rep_fitness.append(temp_fit)
		rep_best.append(temp_best.fitness)
		rep_sigmas.append(sigmas)
		times.append(t)

	rep_iterations = np.array(rep_iterations)
	rep_fitness = np.array(rep_fitness)
	rep_best = np.array(rep_best)
	rep_sigmas = np.array(rep_sigmas)

	section = len(rep_iterations[0])/10

	avg_iters = []
	avg_fitness = []
	avg_sigmas = []
		
	for i in range (0,len(rep_iterations[0]),int(section)): 
		avg_iters.append(i)
		avg_fitness.append(sum(np.take(rep_fitness,i,axis=1))/len(rep_fitness))
		avg_sigmas.append(sum(np.take(rep_sigmas,i,axis=1))/len(rep_sigmas))

	return np.array(avg_iters), np.array(avg_fitness), np.array(rep_best), np.array(avg_sigmas), sum(times)/repetitions


if __name__ == '__main__':
	

	# ESMuPlusLambda(# function, function_range, mu_valure, lambda_value, rho_value (size of the parents selection), m : iterations threshold, dimention of the domain)

	#algo = ESMuPlusLambda(functions.ackley,(-30,30), 20, 100, 5, 10,10)

	
	#best, iterations, fitnesss = algo.execute(100)
	#info = [iterations,fitnesss]
	#print(best)
	
	avg_iterations, avg_fitness, bests_of_all, sigmas = execute_repetitve(10,100)

	data = (avg_iterations, avg_fitness)
	print(bests_of_all)
	print(avg_iterations)
	print(avg_fitness)
	draw_graph_pertubations_comparations(data)
	#print(algo.get_the_best())
	#print(">>>>>>>>>>>>>>>>>>>>>>>")
	#print(best)
	#pop = algo.random_pop_generator()
	#parents = algo.parents_selection()
	#offspring = algo.intermediate_offspring()
	#algo.print_current_pop(offspring)
	#offspring = algo.generate_offspring(, parents)
	#print(pop)
	