import os  #Biblioteca para leer archivos 
import itertools as it #Biblioteca para generar permutaciones 
import math 
import random as rnd

def read_knapsack_file(relative_path):
    '''
    Funcion que recive la ruta relativa de un archivo .txt ejemplo para el problema 0-1 knapsack 
    y regresa un conjunto de datos. 

    Arguments : 
    relative_path

    Returns : 
    n -> numero de elementos : int
    c -> capacidad maxima : int
    id_arr -> arreglo de id's : list<int>
    p_arr -> arreglo de beneficio aportado por el item : list<int> 
    w_arr -> arreglo de pesos : list<int>
    '''

    #Generamos la ruta 
    #Ejemplo de ruta relativa : '/data/ejeL14n45.txt'
    path = os.getcwd()+relative_path

    #Lista donde guardamos las lineas del archivo
    strings = []
    #Lista donde guardamos listas con cada numero como cadena
    characters = []

    #Poblamos la lista de strings 
    with open(path) as f:
        for line in f:
            strings.append(line.strip())
    #Poblamos la lista de characters 
    for line in strings : characters.append(line.split()) 

    #Inicializamos los valores a regresar 
    #Numero de elementos n 
    n=0
    #Arreglo para guardar los id's 
    id_arr =[]
    #Arreglo para guardar los beneficios 
    p_arr = []
    #Arreglo para guardar los pesos 
    w_arr = []
    #Capacidad de la mochila 
    c=0 

    #Poblamos los arreglos 
    for i in range(len(characters)):
        if(i==0):
            n=int(characters[i][0])
        
        elif(i==len(characters)-1):
            c=int(characters[i][0])
        else:
            id_arr.append(int(characters[i][0]))
            p_arr.append(int(characters[i][1]))
            w_arr.append(int(characters[i][2]))

    #Regresamos una tupla n : numero de elementos, c : capacidad , id_arr : id's, p_arr : beneficios, w_arr: pesos 
    return [n,c,id_arr,p_arr,w_arr]

def knapsack_schema(data):
    '''
    Funcion que recibe la tupla de datos regresada por la funcion read_knapsack_file y regresa una representacion 
    del prblema utilizando un esquema de representación con permutaciones, en especifico combinaciones sin repeticion 
    agregando a cada elemento (item) dos valores : contribucion (valor objetivo de cada item) y probabilidad de seleccion,
    la cual se obtiene utilizando seleccion por ruleta. 

    Arguments : 
    n : int 
    c : int 
    id_arr : list<int>
    p_arr : list<int>
    w : list<int>

    Returns : 
    n_elements -> numero de elementos : int 
    capacity -> capacidad : int 
    total_items -> Una lista con toda la informacion de cada item : list<list<int, int, int, float, float>>
    max_value -> Suma de todos los valores : int 
    '''

    n_elements, capacity, id_arr, values_arr, weights_arr = data[0], data[1], data[2], data[3], data[4] 
    
    #Declaramos nuestro arreglo principal de items  
    total_items = []

    #Guardamos la suma total de valores 
    max_value = sum(values_arr)

    #Ahora, para cada item generamos su valor de contribucion 
    contribution_arr = []
    for i in range(len(id_arr)):
        contribution_arr.append(values_arr[i]/weights_arr[i])

    #Ahora, para cada item generamos su probabilidad de ser seleccionado para la solucion inicial 
    prob_selection_arr = []
    #Primero es necesario obtener la suma total de todas las contribuciones 
    sum_contribution = sum(contribution_arr)
    #Procedemos a asignarles la probabilidad 
    for i in range(len(id_arr)):
        #
        prob_selection_arr.append(n_elements/2*(contribution_arr[i]/sum_contribution))

    #Poblamos el arreglo 
    for i in range(len(id_arr)):
        total_items.append([id_arr[i], values_arr[i], weights_arr[i], contribution_arr[i], prob_selection_arr[i]])

    return [n_elements,capacity,max_value,total_items]

#REGISTRAR EN REPORTE Y BORRAR 
# Con esta función le asignamos a cada item una razón de contribución basada en divir el beneficio que el item aporta sobre el peso 
# Si el peso es mayor que el valor , la contribución será poca 
# Si el valor es mayor que el peso, la contribución será mayor 
# Si el peso es muy pequenio la contribución será mayor 
def _contribution_ratio(value, weight):
    return value/weight

def random_knapsack_solution_generator(total_items):
    '''
    Funcion que regresa una solucion (combinacion) al problema que no necesariamente es valida. 
    Basandonos en el operador de selccion por ruleta, a cada item se le asigna una probabilidad 
    de ser seleccionado en base a su contribucion. 

    Arguments: 
    total_items -> el conjunto total de items para generar la solucion : list<list<int, int, int, float, float>>
    
    Returns: 
    random_solution -> una solucion generada por medio de seleccion por ruleta : list<int, int, int, float, float>

    '''
   
    random_solution = []

    for item in total_items: 
        ##Si el numero aleatorio es menor a la probabilidad del item, agregamos el item a la solucion 
        
        if   rnd.uniform(0,1) < item[4]:
            ##Aqui podríamos verificar que el peso del item seleccionado no exceda la capacidad, sin embargo 
            # si hicieramos eso, en el peor de los casos los primeros n-1 items son seleccionados y el n-esimo 
            # siempre queda fuera por que la capacidad ya se llenó.  
            random_solution.append(item)

    return random_solution


def valid_random_knapsack_solution_generator(schema):
    '''
    Funcion que regresa una solucion (combinacion) al problema que es valida. Para esta funcion restringimos 
    que la el peso total de la solucion generada con la funcion random_knapsack_solution_generator no exced la capacidad

    Arguments: 
    schema -> el conjunto de datos :
        n_elements -> numero de elementos : int 
        capacity -> capacidad : int 
        max_value -> Suma de todos los valores : int 
        total_items -> Una lista con toda la informacion de cada item : list<list<int, int, int, float, float>>

    Returns: 
    random_solution -> una solucion valida generada por medio de seleccion por ruleta : list<int, int, int, float, float>s

    '''
    capacity = schema[1]
    
    while(True):
        current_sol = random_knapsack_solution_generator(schema[3])

        current_sol_weight = get_solution_weight(current_sol)

        #Si la capacidad de la solcion generada es menor a la capacidad maxima entonces es candidata a solucion inicial valida 
        if current_sol_weight < capacity:  
            return current_sol


def fitness(solution,max_value):
    '''
    Devuelve el valor objetivo de la funcion basandose minimizar la perdida respecto al valor totarl 
    Arguments: 
    solution -> solucion : list<list<int, int, int, float, float>>
    max_value -> la suma total de todos los valores : int 

    Returns : 
    fitness -> fitness : int
    
    '''
    return max_value-get_solution_value(solution)

def get_solution_value(solution):
    '''
    [AUXILIAR] Funcion que devuelve el valor total de los items de una solucion 
    Arguments: 
    solution -> solucion : list<list<int, int, int, float, float>>

    Returns : 
    value -> valor total : int
    '''
    value = 0

    for item in solution:
        value += item[1]

    return value


def get_solution_weight(solution):
    '''
    [AUXILIAR] Funcion que regresa el peso de una solucion
    
    Arguments: 
    solution -> solucion : list<list<int, int, int, float, float>>

    Returns : 
    weight -> peso de la solucion : int 

    '''
    weight = 0

    for item in solution:
        weight += item[2]

    return weight

def get_best_item(items):
    '''
    [AUXILIAR] Funcion que obtiene el mejor item de una lista de items basandose en la probabilidad de cada uno de ellos  

    Arguments: 
    items -> lista de items : list<list<int, int, int, float, float>>

    Returns : 
    item -> el item seleccionado : list<int, int, int, float, float>
    '''
    for item in items : 
        if rnd.uniform(0,1) < item[4]:
            return item


def get_set_difference(solution, total_items): 
    '''
    [AUXILIAR] Funcion que regresa la diferencia de conjuntos de dos listas, funciona especialmente 
    para determinar los elementos del conjunto general de items que no estan en la solucion recibida 

    Arguments: 
    solution -> solucion : list<list<int, int, int, float, float>>
    total_items -> conjunto completo de items : list<list<int, int, int, float, float>>

    Returns : 
    left -> la diferencia de los dos conjuntos : list<list<int, int, int, float, float>>
    '''
    solution_set = set([tuple(lst) for lst in solution])
    search_space_set = set([tuple(lst) for lst in total_items])
    left = [list(t) for t in search_space_set - solution_set]

    return left 


def get_neighbor(solution, total_items, capacity):
    '''
    [AUXILIAR]  
    Arguments : 
    solution -> solucion para la que se busca un vecino : list<list<int, int, int, float, float>>
    total_items -> el conjunto total de items : list<list<int, int, int, float, float>>
    capacity -> la capacidad total : int 
    
    Returns : 
    neighbor -> vecino encontrado que puede o no ser valido : list<list<int, int, int, float, float>> 
    
    '''
    #Obtenemos los items que no están en la solucion 
    left = get_set_difference(solution,total_items)
    #Obtenemos un item de forma aleatoria 
    new_item = rnd.choice(left)
    #Generamos el vecinos
    neighbor = solution.copy()

    if get_solution_weight(solution) < capacity: 
        neighbor.append(new_item)
        return neighbor
    else: 
        #Obtenemos un item aleatorio para ser sustituido en el vecino 
        deleted_item = rnd.choice(neighbor)
        neighbor.remove(deleted_item)
        #Agregamos el nuevo item 
        neighbor.append(new_item)
        return neighbor


def generate_neighborhood(solution, total_items, capacity, epsilon):
    '''
    [AUXILIAR]Funcion que genera una vecindad de vecinos igual a episilon 
    Arguments : 
    solution -> solucion para la que se busca la vecindad: list<list<int, int, int, float, float>>
    total_items -> el conjunto total de items : list<list<int, int, int, float, float>>
    capacity -> la capacidad total : int 
    epsilon -> distancia (en este caso cantidad de vecinos a generar) : int 
    
    Returns : 
    neighborhood -> Vecindad generada : list<list<list<int, int, int, float, float>>> 
    '''
    neighborhood =[]
    for i in range(epsilon):
        neighborhood.append(get_neighbor(solution, total_items, capacity))

    return neighborhood

def neighborhood_operator(solution, total_items, capacity, epsilon,max_value):
    '''
    Operador de vecindad, recibe una solucion y basandose en mayor descenso regresa un vecino elegido 
    para ser la nueva solucion

    Arguments:
    solution -> solucion para la que se busca la vecindad: list<list<int, int, int, float, float>>
    total_items -> el conjunto total de items : list<list<int, int, int, float, float>>
    capacity -> la capacidad total : int 
    epsilon -> distancia (en este caso cantidad de vecinos a generar) : int 
     
    Returns: 
    new_solution -> solucion elegida por mayor descenso en la vecindad : list<list<int, int, int, float, float>>
    '''
    #Puede pasar que ningun vecino mejore la solcion ?  

    #Obtenemos la vecindad de la solucion recibida 
    neighborhood = generate_neighborhood(solution,total_items,capacity,epsilon)

    #Buscamos al mejor vecino  
    new_solution = solution.copy()

    
    for neighbor in neighborhood:
        if fitness(neighbor,max_value) <= fitness(new_solution,max_value):
            new_solution = neighbor.copy()
    

    #Puede que ninguna de las soluciones sea mejor, en tal caso regresamos la misma solucion 
    if new_solution == []:
        return solution
    
    return new_solution



if __name__ == '__main__': 
    ejemplar_2 = read_knapsack_file('/data/ejeL1n10.txt')
    ejemplar_7 = read_knapsack_file('/data/ejeL10n20.txt')
    ejemplar_1 = read_knapsack_file('/data/ejeL14n45.txt')
    ejemplar_3 = read_knapsack_file('/data/ejeknapPI_11_20_1000_100.txt')
    ejemplar_4 = read_knapsack_file('/data/ejeknapPI_1_50_1000000_14.txt')
    ejemplar_8 = read_knapsack_file('/data/ejeknapPI_3_200_1000_14.txt')
    ejemplar_9 = read_knapsack_file('/data/ejeknapPI_13_100_1000_18.txt')
    ejemplar_5 = read_knapsack_file('/data/eje1n1000.txt')
    ejemplar_6 = read_knapsack_file('/data/eje2n1000.txt')
    #print(ejemplar_8)


    #El esquema debe regresar el valor total 
    elementos, capacidad, valor_maximo, espacio_busqueda= knapsack_schema(ejemplar_1)

    print("----------------")
    print("ITEMS TOTALES")
    for item in espacio_busqueda :
        print(item)

    
    print("----------------")
    #solution = random_knapsack_solution_generator(espacio_busqueda)
   
    print("----------------")
    print("SOLUCION VALIDA")
    valid_solution = valid_random_knapsack_solution_generator(knapsack_schema(ejemplar_1))
    for item in valid_solution :
        print(item)
    print("----------------")
    print("Solution weight")
    print(get_solution_weight(valid_solution))
    print("Items totales")
    print(len(valid_solution))
    print("Fitness de la solucion")
    print(fitness(valid_solution, valor_maximo))
    print("----------------")
    
    print("Obtiene nueva solucion")
    print("----------------")
    nueva_solucion = neighborhood_operator(valid_solution,espacio_busqueda,capacidad,5,valor_maximo)
    for item in nueva_solucion: 
        print(item)
    print("Solution weight")
    print(get_solution_weight(nueva_solucion))
    print("Items totales")
    print(len(nueva_solucion))
    print("Fitness de la solucion")
    print(fitness(nueva_solucion, valor_maximo))

    print("----------------")
    #get_mayor_neighborhood(neighbor,get_set_difference(valid_solution,espacio_busqueda))

    #print("----------------")
    #for item in solution :
        #print(item)

    #random = random_knapsack_solution_generator(espacio_busqueda, 5)
    #math.ceil(elementos/4)
    #print(random)
    #print("----------------")
    #print(len(solution))
    #print("of ")
    #print(elementos)