import writer as w 
import es_mu_plus_lambda as es 
import matplotlib.pyplot as plt


def draw_graph_pertubations_comparations(data_1):



    #Fitness data 1 
    line_1, = plt.plot(data_1[0],data_1[1],color='green', marker='o', linestyle='solid', label='Fitness') 
    #Sigma data 1 
    line_2, = plt.plot(data_1[0],data_1[2],color='green', marker='o', linestyle='dashed', label='Sigma')

    #plt.title("Nombre : {} \nTamanio ejemplar : {} \nFuerza de Perturbacion : {} \nMejor Solucion por perturbacion aleatoria: {}\nMejor Solucion por perturbacion por Frecuencia: {} ".format(name,size,eta,best[0],best[1]), loc = 'left')
    plt.xlabel("Iterations")
    #plt.ylabel("Fitness - Sigma Evolution")
    plt.legend()
    #plt.legend(['Random Perturbation', 'Frecuency Perturbation'])
    plt.show()


def draw_individual(data):

    line_1, = plt.plot(data[0],data[1],color='red', linestyle='solid', label='Fitness')
    line_1, = plt.plot(data[0],data[2],color='black', linestyle='dashed', label='Sigma')

    plt.ylabel("Fitness - Sigma Evolution")
    plt.xlabel("Iterations")

    plt.legend()

    plt.show()

def recombination_comparation(data_1, data_2, best):

    plt.title("Best of Discrete Recombination : {} \nBest of Intermediate Recombination : {}".format(best[0],best[1]))

    #Fitness data 1 
    line_1_f, = plt.plot(data_1[0],data_1[1],color='red', marker='o', linestyle='solid', label='Discrete Fitness') 
    #Sigma data 1 
    line_1_s, = plt.plot(data_1[0],data_1[2],color='red', marker='o', linestyle='dashed', label='Discrete Sigma')

    #Fitness data 2 
    line_2_f, = plt.plot(data_2[0],data_2[1],color='blue', marker='o', linestyle='solid', label='Intermediate Fitness') 
    #Sigma data 1 
    line_2_s, = plt.plot(data_2[0],data_2[2],color='blue', marker='o', linestyle='dashed', label='Intermediate Sigma')

    #plt.title("Nombre : {} \nTamanio ejemplar : {} \nFuerza de Perturbacion : {} \nMejor Solucion por perturbacion aleatoria: {}\nMejor Solucion por perturbacion por Frecuencia: {} ".format(name,size,eta,best[0],best[1]), loc = 'left')
    plt.xlabel("Iterations")
    #plt.ylabel("Fitness - Sigma Evolution")
    plt.legend()
    #plt.legend(['Random Perturbation', 'Frecuency Perturbation'])
    plt.show()

if __name__ == '__main__':


    ind_best ,ind_iter, ind_fit, nd_sigma  = es.execute_single(100,1)

    data_ind = ([ind_iter,ind_fit,nd_sigma])
    draw_individual(data_ind)

    iterations_d, avg_fitness_d, all_bests_d, avg_sigmas_d = es.execute_repetitve(5, 100,0)
    iterations_i, avg_fitness_i, all_bests_i, avg_sigmas_i = es.execute_repetitve(5, 100,1)


    the_bests = (min(all_bests_d), min(all_bests_i))

    #iterations = iterations.tolist()    
    #w.writer("output", "ackley__2.txt", data)

    data_1= (iterations_d,avg_fitness_d,avg_sigmas_d)
    data_2 = (iterations_i, avg_fitness_i,avg_sigmas_i)

    #draw_graph_pertubations_comparations(data_1)

    #recombination_comparation(data_1,data_2,the_bests)

    #w.writer("output", "ackley__2.txt", [iterations.tolist(),avg_fitness.tolist(),all_bests.tolist(),avg_sigmas.tolist()])

    #data = w.reader("output", "ackley__2.txt")
    #print(len(data))
    #print(data[0])
    #print(data[1])
    #print(len(data))
