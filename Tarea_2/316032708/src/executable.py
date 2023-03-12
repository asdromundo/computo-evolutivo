import sys
import knapsack as knap
import knapsack_reader as kr
import simulated_annealing

if __name__ == '__main__': 

    

    paths = ['/data/ejeL1n10.txt',
              '/data/ejeL10n20.txt', 
              '/data/ejeL14n45.txt', 
              '/data/ejeknapPI_11_20_1000_100.txt',
              '/data/ejeknapPI_1_50_1000000_14.txt', 
              '/data/ejeknapPI_3_200_1000_14.txt',
              '/data/ejeknapPI_13_100_1000_18.txt',
              '/data/eje1n1000.txt',
              '/data/eje2n1000.txt']
    
    exemplars = [ kr.read_knapsack_file(paths[i]) for i in range(len(paths)) ]


    dic_exemplars = dict()
    for i in range(len(exemplars)):
        dic_exemplars[i] = exemplars[i]


    n, c, ids, vals, ws = dic_exemplars[int(sys.argv[1])]
    schema = knap.Knapsack( n, c, ids, vals, ws)

    ##Pruebas 
    #sol_ex = schema.generate_random_sol() 
    #epsilon = 5 
    #print("La vecindad de esa solucion con tamanio {}  es: ".format(epsilon))
    #vecindad = schema.generate_neighborhood(sol_ex,5)
    #[print(str(s)+'\nFitness :{}'.format(schema.get_fitness_sol(s))+'\n Weight :{}'.format(schema.get_weight_sol(s)) ) for s in vecindad]

    recocido = simulated_annealing.SimAnnealing(schema,10)
    recocido.execute()