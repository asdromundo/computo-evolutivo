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

		vectors = np.array([np.array([np.random.uniform(self.func_range[0], self.func_range[1]) for i in range(self.dim)]) for j in range(self.mu)])
		population = np.array([ind.ESIndividual(vector,self.sigma, self.function, self.func_range) for vector in vectors])
		#return population 
		self.current_p = population 

	def parents_selection(self): 
		return np.random.choice(self.current_p,size=self.rho, replace=False)


if __name__ == '__main__':
	
	algo = ESMuPlusLambda(functions.ackley,(-30,30), 10, 20, 5, 100, 10, 0.5)
	pop = algo.random_pop_generator()
	#print(pop)
	algo.evaluate_pop()
	algo.print_current_pop(algo.current_p)
	print(">>>>>>>>>>>")
	parents = algo.parents_selection()
	algo.print_current_pop(parents)
