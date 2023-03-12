import knapsack as kp 
import math 
import random as rnd

class SimAnnealing():
    '''
    Clase que modela el recocido simulado, recibe un ejemplar del problema Knapsack
    '''


    def __init__(self, knap, t_init) -> None:
        self.knapsack = knap
        self.temperature = t_init
        self.max_iterations = 1000
        
        self.kp_epsilon = 5 
        self.cooling_betha = 0.01
        
        self.current_sol = []

        self.best_sol = []
        self.worts_sol = []
        self.average_sol = []
    
    #Implementacion de mayor descenso 
    def further_decline(self, sol):  
        #Obtenemos la vecindad de la solucion   
        neighborhood = self.knapsack.generate_neighborhood(sol,self.kp_epsilon)
        #Vamos a tomar al mejor de la vecindad  
        best = neighborhood[0]
        for neighbor in neighborhood:
            if self.knapsack.get_fitness_sol(neighbor) <= self.knapsack.get_fitness_sol(best):
                best = neighbor
        
        return best 

    def prob(self,next_sol):
        
        ####ESTO HAY QUE REVISARLO POR QUE EN NUESTRA FUNCION FITNES MIENTRAS MENOR MEJOR 
        return math.pow(math.e, -( ( self.knapsack.get_fitness_sol(next_sol) - self.knapsack.get_fitness_sol(self.current_sol))/self.temperature ) )

    
    def slow_cooling_schema(self):
        # T = T / (1 + betha * T)
        # betha : 0.001, 0.005, 0.01
        self.temperature = self.temperature / 1+ self.cooling_betha*self.temperature


    def execute(self): 

        
        self.current_sol = self.knapsack.generate_random_sol()

        for i in range(self.max_iterations):
            #La solucion inicial se genera de forma aleatoria 
            #Inicializamos los valores de la mejor y peor solucion 
            #self.best_sol = self.current_sol.copy() 
           # self.worts_sol = self.current_sol.copy()
            #Hay que encontrar el promedio pero para eso hay que guardar todas las soluciones 

            #Obtenemos al vecino de la solucion actual con descenso mayor 
            temp_sol = self.further_decline(self.current_sol)
            if self.knapsack.get_fitness_sol(temp_sol) <= self.knapsack.get_fitness_sol(self.current_sol):
                self.current_sol = temp_sol
            elif rnd.uniform(0,1) < self.prob(temp_sol):
                self.current_sol = temp_sol

        
            print(self.current_sol)
            print('Fitness de la solucion actual :{} '.format(self.knapsack.get_fitness_sol(self.current_sol)))
            print('Peso de la solucion actual: {}'.format(self.knapsack.get_weight_sol(self.current_sol)))
            
            self.slow_cooling_schema()
        
        print('Maximo valor : {}'.format(self.knapsack.max_value))
        print('Capacidad Maxima : {}'.format(self.knapsack.max_value))


        return self.current_sol

        



    
