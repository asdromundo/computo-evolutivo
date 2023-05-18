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
	func_range = (float , float)
		the domain of the funtion 
	//Es posible que valga la pena agregar el rango de la funcion y una funcion de la clase que repare el vector 

	'''
	def __init__(self, vec, sig, fun, rg):

		self.vector= vec
		self.sigma=sig  
		self.function = fun 
		self.func_range = rg 
		self.fitness = 0 

	def evaluate(self): 

		self.fitness = self.function(self.vector)
		#self.fitness = fun(self.vector)

	def increase_sigma(self,c):
		self.sigma = c*c*self.sigma

	def decrease_sigma(self,c):
		self.sigma = self.sigma/c

if __name__ == '__main__':

	ind = ESIndividual([1,2,3,4], 0.5,functions.ackley,(-30,30))
	print(ind.fitness)
	ind.evaluate()
	print(ind.fitness)
	#print(funtions.ackley(np.array([1,2])))