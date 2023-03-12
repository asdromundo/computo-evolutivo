import itertools as it #Biblioteca para generar permutaciones 
import math 
import random as rnd
import sys

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
    total_items : list : list : [id : int, beneficio : int, peso : int]
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
        '''
        Genera una solcion aleatoria, por cada item hay una probabilidad de .5 de que sea seleccionado para la solucion 

        Returns:
        sol : list : list : [id : int, beneficio : int, peso : int] 
            solucion generada aleatoriamente con probabilidad .5 
        '''
        return [item for item in self.total_items if rnd.uniform(0,1) < .5]
    
    def get_fitness_sol(self, sol): 
        '''
        Devuelve el valor objetivo de la funcion basandose minimizar la perdida respecto al maximo beneficio
        
        Args : 
        sol : list : list : [id : int, beneficio : int, peso : int] 
            solucion a evaluar 

        Returns: 
        fitness : int 
            Valor objetivo de la solucion sol 
        '''
        return self.max_value - sum([item[1] for item in sol])

    def get_weight_sol(self, sol):
        '''
        Devuelve el peso dada una solucion 

        Args:
        sol : list : list : [id : int, beneficio : int, peso : int] 
            solucion a evaluar  

        Returns: 
        wieght : int 
            Peso total de la solucion sol 
        '''
        return sum(item[2] for item in sol)
    
    def get_diff_items(self, sol):
        '''
        Devuelve los items que estan en el conjunto inicial de items y que no estan en la solucion 

        Args:
        sol : list : list : [id : int, beneficio : int, peso : int]
            solucion a la que restar items del conjunto total de items 
        
        Returns: 
        diff : list : list : [id : int, beneficio : int, peso : int]
            Diferencia entre el conjunto total de items y la solucion recibida sol 
        '''
        sol_set = set([tuple(lst) for lst in sol])
        return [list(item) for item in self.items_set - sol_set]

    def get_neighbor(self,sol):
        '''
        Genera un vecino de la solucion recibida. Si el peso total de la solucion recibida 
        no excede la capacidad maxima entonces se agrega un item aleatorio que no tenga la solucion. 
        De otro modo se reemplaza un item aleatorio por algun otro que no tenga la solucion .

        Args:
        sol : list : list : [id : int, beneficio : int, peso : int]
            solucion base para encontrar una solucion vecina     


        '''
        #Obtenemos un item que no este en la solucion 
        diff = self.get_diff_items(sol)
        
        #Puede ocurrir que la solucion contenga todos los elementos, en tal caso regresamos la solucion 
        if(diff == []):
            return sol

        new_item = rnd.choice(diff)
        
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
        '''
        Genera una vecindad para la solucion recibida con una cantidad de vecinos igual a epsilon. 

        Args: 
        sol : list : list : [id : int, beneficio : int, peso : int] 
            solucion base para encontrar una solucion vecina
        epsilon : int 
            numero de vecinos a generar (tamanio de la vecindad)


        Returns: 
        neighborhood : list : list : [id : int, beneficio : int, peso : int]
        '''

        return [self.get_neighbor(sol) for i in range(epsilon)]
