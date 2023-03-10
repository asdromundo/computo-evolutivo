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
    '''

    n_elements, capacity, id_arr, values_arr, weights_arr = data[0], data[1], data[2], data[3], data[4] 
    
    #Declaramos nuestro arreglo principal de items  
    total_items = []

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

    return [n_elements,capacity, total_items]

#REGISTRAR EN REPORTE Y BORRAR 
# Con esta función le asignamos a cada item una razón de contribución basada en divir el beneficio que el item aporta sobre el peso 
# Si el peso es mayor que el valor , la contribución será poca 
# Si el valor es mayor que el peso, la contribución será mayor 
# Si el peso es muy pequenio la contribución será mayor 
def _contribution_ratio(value, weight):
    return value/weight

#REGISTRAR EN REPORTE Y BORRAR 
# Con esta función le asignamos a cada item una probabilidad de ser elegido para la solucion aleatoria inicial basandonos en su contribucion
# vamos a utilizar el operador de seleccion por ruleta para algoritmos geneticos https://en.wikipedia.org/wiki/Fitness_proportionate_selection
# De este modo, cada item en la mochila tendrá una probabilidad de ser elegido para la solucion aleatoria proporcional a su razon de contribucion 
def _prob_selection(contribution, total_contribution):
    return contribution/total_contribution


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
    schema -> el conjunto de datos 
    n_elements -> numero de elementos : int 
    capacity -> capacidad : int 
    total_items -> Una lista con toda la informacion de cada item : list<list<int, int, int, float, float>>

    Returns: 
    random_solution -> una solucion valida generada por medio de seleccion por ruleta : list<int, int, int, float, float>s

    '''
    capacity = schema[1]
    
    while(True):
        current_sol = random_knapsack_solution_generator(schema[2])

        current_sol_weight = get_solution_weight(current_sol)

        #Si la capacidad de la solcion generada es menor a la capacidad maxima entonces es candidata a solucion inicial valida 
        if current_sol_weight < capacity:
            #BORRAR
            print(current_sol_weight) 
            print("OF")
            print(capacity)
            
            return current_sol


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

def get_worst_item(solution):
    '''
    [AUXILIAR] Funcion que recibe una solucion y regresa el item con peor contribucion, es decir el item de menor contribucin 
    
    Arguments: 
    solution -> solucion : list<list<int, int, int, float, float>>

    Returns: 
    item : list<int, int, int, float, float>
    '''

    #Recordemos que la contribucion se guarda en el indice 3 
    worst_solution = solution[0]

    for item in solution:
        if item[3] < worst_solution[3]:
            worst_solution = item

    return worst_solution


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


def get_mayor_neighborhood(item, total_items): 
    '''
    [AUXILIAR] Funcion que encuentra los mejores candidatos para sustituir un item recibidos basandose 
    en la contribucion y elije a un de ellos basandose en su probabilidad  

    Arguments: 
    item -> el item n de la cual buscar posibles reemplazos : list<int, int, int, float, float>
    total_items ->  conjunto completo de items :  list<list<int, int, int, float, float>>

    Returns : 
    best_candidate
    '''
    best_candidates = []
    for candidate in total_items: 
        print(type(candidate))
        if candidate[3] > item[3]:
            best_candidates.append(candidate)

    print("-------------")
    print("VERIFICANDO POSIBLES CANDIDATOS BASADOS EN LA CONTRIBUCION ")
    print("ITEM A REEMPLAZAR :")
    print(item) 
    print("MEJORES CANDIDATOS")
    for i in best_candidates : 
        print(i)
    print("-------------")

#Cómo va a funcionar el operador de vecindad ? 
# Para la solucion actual hay que revisar el peso total, si el peso total es menor entonces podemos agregar un nuevo item que NO ESTE en la solucion actual 
# tenemos que considerar de alguna forma la razon 
# Para seleccionar un nuevo item hay que volver a calcular la probabilidad ? (esto sería lo más optimo )
# Ya que se seleccionó el nuevo item preguntamos : el peso de la solucion actual + el peso del nuevo item < capacidad 
#       SI : Entonces regresamos esa nueva solución 
#       NO : Entonces descartamos ese item , pero como la solución es valida (no excede la capacidad) entonces es posible que mejore 
#            Hay que buscar al item tal de menor contribucion , lo fijamos y ahora en los items restantantes vamos a generar un conjunto de los items 
#            con contribución menor al item fijado, si ese conjunto es vacio regresamos la solucion, si no es vacio entonces elegimos uno de esos items 
#            al azar y lo regresamos (Hay que notar que la solucion que regresamos no necesariamente es valida)
# Revisar si es mayor descenso o primer descenso  

# Tal vez necesitamo una funcion que reciba un arreglo de items con su fitness asociada y que devuelva uno de ellos 
def get_neighbor(solution, total_items, capacity):
    '''
    Una funcion que recibe una solucion, un conjunto de items y una capacidad y regresa un vecino de esa solucion 

    Arguments : 
    solution -> solucion para la que se busca un vecino : list<list<int, int, int, float, float>>
    total_items -> el conjunto total de items : list<list<int, int, int, float, float>>
    capacity -> la capacidad total : int 
    
    Returns : 
    neighbor -> vecino encontrado que puede o no ser valido : list<list<int, int, int, float, float>> 
    '''
    

    neighbor = solution.copy()

    if get_solution_weight(solution) > capacity : 
        print("El peso total de la solucion supera la capacidad, se regresa la misma solucion")
        return solution

    #Determinamos la diferencia entre la solucion y el total de items , es decir los items restantes que pueden ser considerados 
    left = get_set_difference(solution, total_items)
    
    #solution_set = set([tuple(lst) for lst in solution])
    #search_space_set = set([tuple(lst) for lst in total_items])
    #left = [list(t) for t in search_space_set - solution_set]

    #Aqui podríamos tomar al item con menor ranzon, entonces estamos haciendo mayor descenso s
    
    #Como el peso total de la solucion recibida no excede la capacidad entonces es posible que podamos agregar un elementos más a la solucion 
    #Vamos a considerar las mismas probabilidades que obtuvimos desde el equema, aquellos items con probabilidad tendrás más posibilidades 
    #Este paso sería muy cercano a MAYOR DESCENSO por que connsideramos a todas las soluciones y las que tienen mejor contribucion tienen mayor probabilidad de ser seleccionados
    new_item = get_best_item(left)
    
    #Agregamos el nuevo item a la solucion 
    neighbor.append(new_item)

    if get_solution_weight(neighbor) < capacidad : 
        #Si el peso de la nueva solucion es menor a la capacidad entonces regresamos esa solucion
        return neighbor
    else: 
        #Si el peso es mayor o igual a la capacidad, entonces es posible que se pueda mejorar la solucion 
        #sustituyendo el elemento con menor contribucion por algun candidato que tenga mejor contribucion  
        # 1: Encontrar al elemento de menor contribucion  "X" : get_worst_item
        # 2: Determinar un conjunto de items "C" que son mejores que "X" , es decir que tienen mejor contribucion 
        # 3: Seleccionar uno de los items considerando la probabilidad del conjunto total, sea "Y"  
        # 4: Agregar Y a nuestra solucion  
        # 5: Aqui podríamos regresar la solucion o revisar si sigue siendo valida 
        #return
        print("Esto se murio") 

    return neighbor

    






if __name__ == '__main__': 
    ejemplar_1 = read_knapsack_file('/data/ejeL14n45.txt')
    ejemplar_2 = read_knapsack_file('/data/ejeL1n10.txt')
    ejemplar_3 = read_knapsack_file('/data/ejeknapPI_11_20_1000_100.txt')
    ejemplar_4 = read_knapsack_file('/data/ejeknapPI_1_50_1000000_14.txt')
    ejemplar_8 = read_knapsack_file('/data/ejeknapPI_3_200_1000_14.txt')
    ejemplar_9 = read_knapsack_file('/data/ejeknapPI_13_100_1000_18.txt')
    ejemplar_5 = read_knapsack_file('/data/eje1n1000.txt')
    ejemplar_6 = read_knapsack_file('/data/eje2n1000.txt')
    ejemplar_7 = read_knapsack_file('/data/ejeL10n20.txt')
    #print(ejemplar_8)

    elementos, capacidad, espacio_busqueda= knapsack_schema(ejemplar_1)

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
    print("----------------")
    
    best_neighbor = get_neighbor(valid_solution, espacio_busqueda, capacidad)
    print("----------------")
    print("Best neighbor")
    for item in best_neighbor:
        print(item)
    print("Solution weight")
    print(get_solution_weight(best_neighbor))
    print("Items totales")
    print(len(best_neighbor  ))
    print("----------------")

    get_mayor_neighborhood(best_neighbor,get_set_difference(valid_solution,espacio_busqueda))

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