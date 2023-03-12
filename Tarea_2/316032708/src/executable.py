import sys
import pandas as pd 

import knapsack as knap
import knapsack_reader as kr
import simulated_annealing


if __name__ == '__main__': 

    

    paths = ['/data/ejeL1n10.txt', #0
              '/data/ejeL10n20.txt', #1
              '/data/ejeL14n45.txt', #2
              '/data/ejeknapPI_11_20_1000_100.txt',#3
              '/data/ejeknapPI_1_50_1000000_14.txt', #4
              '/data/ejeknapPI_3_200_1000_14.txt',#5
              '/data/ejeknapPI_13_100_1000_18.txt',#6
              '/data/eje1n1000.txt',#7
              '/data/eje2n1000.txt']#8
    
    exemplars = [ kr.read_knapsack_file(paths[i]) for i in range(len(paths)) ]


    dic_exemplars = dict()
    for i in range(len(exemplars)):
        dic_exemplars[i] = exemplars[i]


    n, c, ids, vals, ws = dic_exemplars[int(sys.argv[1])]
    schema = knap.Knapsack( n, c, ids, vals, ws)

    #Ejecucion                                                     
    recocido = simulated_annealing.SimAnnealing(schema,20,6,0.01,3000)
    
    #Maximo valor de la solucion para calcular el mejor y peor valor 
    value = recocido.knapsack.max_value

    #Se almacenan los datos obtenidos
    
    iteraciones = []
    mejores = []
    medios = []
    peores = []

    for i in range(10):
        data = recocido.execute()
        df = pd.DataFrame({"Fitness" : data})
        iteraciones.append(i)
        mejores.append(df["Fitness"].min())
        peores.append(df["Fitness"].max())
        medios.append(df["Fitness"].mean())



    #Muestra de datos 
    print("Ejemplar {}".format(paths[int(sys.argv[1])]))
    print("Maximo beneficio : {}".format(value))
    total_df = pd.DataFrame({"No.Iteracion" : iteraciones, "Mejor":mejores, "Promedio": medios, "Peor":peores})

    print(total_df)
    
