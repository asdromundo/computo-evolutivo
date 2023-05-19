import functions 
import numpy as np
import es_individual as ind 

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

	def __init__(self, fun, fun_rg, mu, lam, rho, m,dim,sigma):
		self.function = fun
		self.func_range = fun_rg
		self.mu = mu	
		self.lamb = lam 
		self.rho = rho
		self.m = m 
		self.dim = dim 
		self.sigma = sigma # REVISAR SI ESTO VA A AQUÍ 
		self.iters = 0  #Iterations counter 
		self.sucess = 0  #Succes counter
		self.current_p = [] #Current population initialized as empty

	def __str__(self):
		return "Mu value : {}".format(str(self.mu))+"\n"+"Lambda value : {}".format(str(self.lamb))+"Dominion Dimention : {}".format(self.dim)

	def print_current_pop(self,pop):
		for ind in pop: 
			print(ind)

	def evaluate_pop(self):
		for ind in self.current_p:
			ind.evaluate()

	#Hay que generar individuos de forma random 	
	def random_pop_generator(self):
		'''
		It generate a random population based on mu individuals and based on the dimension and range of the funtion 
		'''
		vectors = np.array([np.array([np.random.uniform(self.func_range[0], self.func_range[1]) for i in range(self.dim)]) for j in range(self.mu)])
		population = np.array([ind.ESIndividual(vector,self.sigma, self.function, self.func_range) for vector in vectors])
		#return population 
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

		return ind.ESIndividual(np.array(genotype),new_sigma,self.function,self.func_range)

	def  intermediate_recombination(self,parents):

		#We extract the vectors from the parents 
		vector_matrix = np.array([parent.vector for parent in parents])

		#We extract the sigmas from the parents 
		sigmas = np.array([parent.sigma for parent in parents])

		#genotype =[]

		genotype = [((sum(np.take(vector_matrix,i,axis=1)))/self.dim) for i in range(self.dim)]

		new_sigma = sum(sigmas)/len(sigmas)

		return ind.ESIndividual(np.array(genotype),new_sigma,self.function,self.func_range)

	def mutate(self, individual):

		#Generate a random number using normal distribution 
		r = np.random.normal(0,individual.sigma*individual.sigma,len(individual.vector))
		
		#Mutate the indiviual 
		return ind.ESIndividual(individual.vector+r,individual.sigma,self.function,self.func_range)

	def mu_plus_lambda_selection(self, offspring):

		selection_pool = self.current_p + offspring 

		#We select the best mu individuals from the selection pool 
		self.current_p = sorted(selection_pool, key = lambda individual : individual.fitness)[:self.mu]


		
if __name__ == '__main__':
	
	algo = ESMuPlusLambda(functions.ackley,(-30,30), 10, 20, 5, 100, 5, 0.5)
	pop = algo.random_pop_generator()
	#print(pop)
	algo.evaluate_pop()
	algo.print_current_pop(algo.current_p)
	print(">>>>>>>>>>>")
	parents = algo.parents_selection()
	algo.print_current_pop(parents)
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	child = algo.discrete_recombination(parents)
	print(child)
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	child_2 = algo.intermediate_recombination(parents)
	child_2.evaluate()
	print(child_2)
	print("MUTATED CHILD")
	child_2_mutated = algo.mutate(child_2)
	child_2_mutated.evaluate()
	print(child_2_mutated)