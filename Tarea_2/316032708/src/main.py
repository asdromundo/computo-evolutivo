import os  #Biblioteca para leer archivos 
import itertools as it #Biblioteca para generar permutaciones 
import math 
import random as rnd

def read_knapsack_file(relative_path):

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
            ##print(line.strip())
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

    n_elements, capacity, id_arr, values_arr, weights_arr = data[0], data[1], data[2], data[3], data[4] 
    
    #Declaramos nuestro arreglo principal de items  
    search_space = []

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
        #Se multiplica por 50 por que la funcion de 10
        prob_selection_arr.append(n_elements/2*(contribution_arr[i]/sum_contribution))

    #Poblamos el arreglo 
    for i in range(len(id_arr)):
        search_space.append([id_arr[i], values_arr[i], weights_arr[i], contribution_arr[i], prob_selection_arr[i]])

    #Solucionar esto por que estamos regresando 2 veces la capacidad y la cantidad de elementos 
    return [n_elements,capacity, search_space]

# Con esta función le asignamos a cada item una razón de contribución basada en divir el beneficio que el item aporta sobre el peso 
# Si el peso es mayor que el valor , la contribución será poca 
# Si el valor es mayor que el peso, la contribución será mayor 
# Si el peso es muy pequenio la contribución será mayor 
def _contribution_ratio(value, weight):
    return value/weight

# Con esta función le asignamos a cada item una probabilidad de ser elegido para la solucion aleatoria inicial basandonos en su contribucion
# vamos a utilizar el operador de seleccion por ruleta para algoritmos geneticos https://en.wikipedia.org/wiki/Fitness_proportionate_selection
# De este modo, cada item en la mochila tendrá una probabilidad de ser elegido para la solucion aleatoria proporcional a su razon de contribucion 
def _prob_selection(contribution, total_contribution):
    return contribution/total_contribution




# De nuevo, refiriendonos al operador de seleccion de ruleta vamos a generar una solucion basada 
# en la probabilidad que tiene cada item de ser escogido 
# Aqui es importante resaltar que la permutacion [A,B,C] va a tener el mismo valor que [C,B,A]
def random_knapsack_solution(search_space):

    #El search space es el tercer elemento de la tupla de knapsack_schema
    random_solution = []
    #Cumple con capacidad 

    for item in search_space: 
        ##Si el numero aleatorio es menor a la probabilidad del item, agregamos el item a la solucion 
        if   rnd.uniform(0,1) < item[4]: 
            random_solution.append(item)

    return random_solution

    #for i in it.islice(it.combinations_with_replacement(search_space,k), k):
    #for i in it.combinations_with_replacement(search_space,k):    
        #print(i)
    #return rnd.sample(search_space,k)

def valid_random_knapsack_solution(ejemplar):
    
    capacity = ejemplar[1]
    
    current_sol_capacity = 0
    
    while(True):
        current_sol = random_knapsack_solution(ejemplar[2])
        for item in current_sol:
            #Determinamos el "volumen" ocupado por la actual solucion
            current_sol_capacity += item[2]
            
        #Si la capacidad de la solcion generada es menor a la capacidad maxima entonces es candidata a solucion inicial valida 
        if current_sol_capacity < capacity:
            print(current_sol_capacity) #BORRAR 
            print("OF")
            print(capacity)
            return current_sol
        else: #De otoro modo reseteamos la capacidad de la solucion actual y generamos una nueva 
            current_sol_capacity =0
        


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

    for item in espacio_busqueda :
        print(item)

    solution = random_knapsack_solution(espacio_busqueda)
   

    print("----------------")
    print("SOLUCION VALIDA")
    valid_solution = valid_random_knapsack_solution(knapsack_schema(ejemplar_1))
    for item in valid_solution :
        print(item)
    print("----------------")

    
    print("----------------")
    for item in solution :
        print(item)

    #random = random_knapsack_solution(espacio_busqueda, 5)
    #math.ceil(elementos/4)
    #print(random)
    print("----------------")
    print(len(solution))
    print("of ")
    print(elementos)