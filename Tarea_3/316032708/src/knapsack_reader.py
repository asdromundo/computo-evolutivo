import os  #Biblioteca para leer archivos 

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

def read_sample_data(relative_path):
    '''
    Esta funcion recibe la ruta del archivo en donde se guardan las mejores soluciones 
    despues de realizar 30 repeticiones de iterative local search, este archivo contiene 
    una cadena que representa un arreglo de muestras por cada estrategia de perturbacion, 
    para la tarea 3 solo tenemos dos arreglos, el de perturbacion aleatoria y perturbacion 
    por frecuencias.

    Args : 
        
    relative_path : string 
        Ruta relativa del archivo a leer

    Returns 

    samples : list : list : int
        Una lista con las muestras de cada estrategia de perturbacion 

    '''
    path = os.getcwd()+relative_path
    samples = []

    with open(path) as f:
        for line in f:
            samples.append(eval(line))

    return samples  


def write_knapsack_file(relative_path, data):
    '''
    Args: 
    relative_path : string 
        la ruta del archivo a escribir
    data : list : string 
        la lista de datos a escribir 
    
    '''
    #Generamos la ruta 
    #Ejemplo de ruta relativa : '/data/ejeL14n45.txt'
    path = os.getcwd()+relative_path

    with open(path,'w') as f:
        for da in data: 
            f.writelines(da)

