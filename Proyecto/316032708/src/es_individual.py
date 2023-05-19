import functions 
import numpy as np

class ESIndividual: 
	'''
	Class modeling an individual from a ES 


	Attributes : 
	vector : list : float 
		The vector value of dimension n 
	fitness : float 
		The fitness value 
	sigma : float 
		mutation strenght 
	fun : function 
		The function to optimize 
	func_range = (float , float)
		The domain of the funtion 
	//Es posible que valga la pena agregar el rango de la funcion y una funcion de la clase que repare el vector 

	'''
	def __init__(self, vec, sig, fun, rg):

		self.vector= vec
		self.sigma=sig  
		self.function = fun 
		self.func_range = rg 
		self.fitness = 0 

	def __str__(self):
		return "Vector : {}".format(str(self.vector))+"\n"+"Endogenous values : {}".format(str(self.sigma))+"\n"+"Fitness value : {}".format(str(self.fitness))

	def evaluate(self): 
		'''
		Evaluate the solution using the function received in constructor 
		'''
		self.fitness = self.function(self.vector)
		#self.fitness = fun(self.vector)

	def fix_genotype(self):

		'''
		Method to fix the genotype of the individual  
		'''
		for gen in self.vector: 
			if(gen < self.func_range[0]) : gen = self.func_range[0]
			if(gen > self.func_range[1]) :gen = self.func_range[1]

	def increase_sigma(self,c):
		'''
		c : float 
			The change factor received from mutations step 
		'''
		self.sigma = c*c*self.sigma

	def decrease_sigma(self,c):
		'''
		c : float 
			The change factor received from mutations step 
		'''
		self.sigma = self.sigma/c

if __name__ == '__main__':

	ind = ESIndividual([1,2,3,4,5,7,-5], 0.5,functions.ackley,(-30,30))
	print(ind.fitness)
	ind.evaluate()
	print(ind.fitness)
	print(ind)
	#print(funtions.ackley(np.array([1,2])))