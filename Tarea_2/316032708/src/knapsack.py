import itertools as it #Biblioteca para generar permutaciones 
import math 
import random as rnd
import knapsack_reader as kr #Script para leer ejemplares de knapsack  

class Knapsack: 
    '''
    Clase que define un ejemplar del problema de 0-1 Knapsack 

    ...

    Attributes  
    ----------

    number : int
        Numero de elementos del ejemplar 
    capacity : int 
        Capacidad maxima del ejemplar 
    max_value : int 
        Valor maximo del ejemplar, se utiliza para determinar la perdida en la funcion objetivo  
    total_items : list < list <id, beneficio, peso, contribucion, pro_seleccion> >
        Lista de todos los elementos en el ejemplar
    total_items_set : 
        Conjunto que representa a total_items para realizar operaciones de conjuntos
    '''


    def __init__(self, n, c, id_arr, val_arr, w_arr):
        self.number = n 
        self.capacity = c 
        self.max_value = sum(val_arr)
        self.total_items = [[id_arr[i], val_arr[i], w_arr[i]] for  i in range(len(id_arr))]
        
        #Este atributo solo se usa para obtener la diferencia de items dada una solucion con el conjunto total de items 
        self.items_set = set([tuple(lst) for lst in self.total_items])
        

    def generate_random_sol(self): 
        return [item for item in self.total_items if rnd.uniform(0,1) < .5]
    
    def get_fitness_sol(self, sol): 
        return self.max_value - sum([item[1] for item in sol])

    def get_weight_sol(self, sol):
        return sum(item[2] for item in sol)
    
    def get_left_items(self, sol):
        sol_set = set([tuple(lst) for lst in sol])
        return [list(item) for item in self.items_set - sol_set]

    def get_neighbor(self,sol):
        
        #Obtenemos un item que no este en la solucion 
        new_item = rnd.choice(self.get_left_items(sol))
        
        neighbor = sol.copy()
       
        #Si la capacidad no ha sido excedida, podemos agregar mas items 
        if self.get_weight_sol(neighbor) < self.capacity:
            neighbor.append(new_item)
        else : 
            #Borramos un elemento de manera aleatoria 
            neighbor.remove(rnd.choice(neighbor))
            neighbor.append(new_item)

        return neighbor

    def generate_neighborhood(self, sol, epsilon): 

        return [self.get_neighbor(sol) for i in range(epsilon)]


if __name__ == '__main__': 


    ejemplar_1 = kr.read_knapsack_file('/data/ejeL14n45.txt')

    n, c, ids, vals, ws = ejemplar_1

    knapsack_ej = Knapsack(n, c, ids, vals, ws)
    sol_ex = knapsack_ej.generate_random_sol() 

    #print(sol_ex)
    #print('{} of {} Posibles items'.format(len(sol_ex), n))
    #sol_fit = knapsack_ej.get_fitness_sol(sol_ex)
    #print('Fitness funtion : {}'.format(sol_fit))
    #sol_w = knapsack_ej.get_weight_sol(sol_ex)
    #print('La solucion ocupa {} de la capacidad maxima {} '.format(sol_w, c))
    epsilon = 5 
    print("La vecindad de esa solucion con tamanio {}  es: ".format(epsilon))
    vecindad = knapsack_ej.generate_neighborhood(sol_ex,5)
    [print(str(s)+'\nFitness :{}'.format(knapsack_ej.get_fitness_sol(s))+'\n Weight :{}'.format(knapsack_ej.get_weight_sol(s)) ) for s in vecindad]

