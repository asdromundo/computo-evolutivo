import knapsack as kp 
import math 
import random as rnd

class SimAnnealing():
    '''
    Clase que modela el recocido simulado, recibe un ejemplar del problema Knapsack

    Attributes: 

    knap : class Knapsack 
        ejemplar de problema de la mochila 
    t_init : int 
        temperatura inicial 
    kp_ep : int 
        epsilon para determinar cardinalidad del conjunto de vecinos para cada solucion 
    cool_be : float 
        constante para regular la velocidad de enfriamiento usando enfriamiento con decremento lento 

    '''

    def __init__(self, knap, t_init, kp_ep, cool_be,iter) -> None:
        self.knapsack = knap
        self.temperature = t_init
        self.max_iterations = iter
        
        self.kp_epsilon = kp_ep 
        self.cooling_beta = cool_be

        #Variables para registrar soluciones         
        self.current_sol = []
    
    
    def further_decline(self, sol):
        '''
        Estrategia de seleccion de vecinos, la cual usa mayor descenso 

        Args:
        sol : list : list : [id : int, beneficio : int, peso : int] 
            solucion para la cual encontrar el mejor vecino dada una epsilon 

        Returns : 
        best : list : list : [id : int, beneficio : int, peso : int] 
            mejor solucion encontrada en la vecindad de tamanio epsilon 
        '''
        #Obtenemos la vecindad de la solucion   
        neighborhood = self.knapsack.generate_neighborhood(sol,self.kp_epsilon)
        #Vamos a tomar al mejor de la vecindad  
        best = neighborhood[0]
        for neighbor in neighborhood:
            if self.knapsack.get_fitness_sol(neighbor) <= self.knapsack.get_fitness_sol(best):
                best = neighbor
        
        return best 

    def prob(self,next_sol):
        '''
        Probabilidad de aceptacion dada una solucion vecina de la solucion actual 

        Args:
        sol : list : list : [id : int, beneficio : int, peso : int]
            solucion candidata a ser solucion actual 

        Returns 
        proba : float 
            proabilidad de ser aceptada  
        '''    
        ####ESTO HAY QUE REVISARLO POR QUE EN NUESTRA FUNCION FITNES MIENTRAS MENOR MEJOR 
        return math.pow(math.e, -( ( self.knapsack.get_fitness_sol(next_sol) - self.knapsack.get_fitness_sol(self.current_sol))/self.temperature ) )

    
    def slow_cooling_schema(self):
        '''
        Esquema de enfriamiento con decremento lento. Cada iteracion disminuye la temperatura usando el valor de cooling_beta 
        '''
        # T = T / (1 + betha * T)
        # betha : 0.001, 0.005, 0.01
        self.temperature = self.temperature / 1+ self.cooling_beta*self.temperature


    def execute(self): 
        '''
        Ejecucion del algoritmo de Recocido Simulado 
        '''
        #Arreglos de datos 
        fitness_values = []
        #weihts_values = []

        #Generacion de solucion aleatoria inicial 
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

            current_fitness = self.knapsack.get_fitness_sol(self.current_sol)
            
            #print(self.current_sol)
            #print('Fitness de la solucion actual :{} '.format(current_fitness))
            #print('Peso de la solucion actual: {}'.format(self.knapsack.get_weight_sol(self.current_sol)))
            
            fitness_values.append(current_fitness)


            self.slow_cooling_schema()
        
        #print('Maximo valor : {}'.format(self.knapsack.max_value))
        #print('Capacidad Maxima : {}'.format(self.knapsack.max_value))

        
        return fitness_values

        



    
