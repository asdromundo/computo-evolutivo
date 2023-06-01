import writer as w 
import es_mu_plus_lambda as es 
import matplotlib.pyplot as plt


def draw_individual(data):

    line_1, = plt.plot(data[0],data[1],color='red', linestyle='solid', label='Fitness')
    line_1, = plt.plot(data[0],data[2],color='black', linestyle='dashed', label='Sigma')

    plt.ylabel("Fitness - Sigma Evolution")
    plt.xlabel("Iterations")

    plt.legend()

    plt.show()

def recombination_comparation(data_1, data_2, best, worst, times):

    plt.title("Discrete Recombination : Fitness(Best) :{}   Fitness(Worst)  :{}  Time :{}\nIntermediate Recombination : Fitness(Best) :{}  Fitness(Worst) :{}     Time: {}".format(best[0],times[0],worst[0],best[1],worst[1],times[1]))

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

def boxplot(sample_1,sample_2):
    '''
    Generacion de la grafica boxplot para las muestras 
    ''' 
    fig, (ax1, ax2) = plt.subplots(1,2)

    ax1.boxplot(sample_1)
    ax2.boxplot(sample_2)

    ax1.text(1.05, max(sample_1), "Discrete", fontweight="bold", fontsize=12)
    ax2.text(1.05, max(sample_2), "Intermediate", fontweight="bold", fontsize=12)

    # Set y-axis limits to include the labels
    ax1.set_ylim(0, max(sample_1) + 1)
    ax2.set_ylim(0, max(sample_2) + 1)

    #bp = ax.boxplot([sample_1,sample_2],showfliers=False)
    plt.show()

def boxplot_2(sample_1,sample_2):
    '''
    Generacion de la grafica boxplot para las muestras 
    ''' 

    #plt.title("Best of Discrete Recombination : {} \nBest of Intermediate Recombination : {}".format(min(sample_1),min(sample_2)))

    fig, ax = plt.subplots()
    bp = ax.boxplot([sample_1,sample_2],showfliers=False)
    #plt.title("Best of Discrete Recombination : {} \nBest of Intermediate Recombination : {}".format(min(sample_1),min(sample_2)))
    plt.show()


def execute_for_avg():

    iterations_d, avg_fitness_d, all_bests_d, avg_sigmas_d, time_d = es.execute_repetitve(10, 100,0)
    iterations_i, avg_fitness_i, all_bests_i, avg_sigmas_i, time_i = es.execute_repetitve(10, 100,1)

    #boxplot_2(all_bests_d, all_bests_i)


    the_bests = (min(all_bests_d), min(all_bests_i))
    the_worst = (max(all_bests_d), max(all_bests_i))


    print("THE BESTS")
    print("Discrete : {}".format(min(all_bests_d)))
    print("Intermediate : {}".format(min(all_bests_i)))

    print("THE WORTS")
    print("Discrete : {}".format(max(all_bests_d)))
    print("Intermediate : {}".format(max(all_bests_i)))

    print("TIMES")
    print("Discrete : {}".format(time_d))
    print("Intermediate : {}".format(time_i))

    times = (time_d, time_i)

    data_1= (iterations_d,avg_fitness_d,avg_sigmas_d)
    data_2 = (iterations_i, avg_fitness_i,avg_sigmas_i)

    recombination_comparation(data_1,data_2,the_bests,the_worst, times)
    boxplot_2(all_bests_d, all_bests_i)

def execute_for_ind():

    ind_best ,ind_iter, ind_fit, nd_sigma, t= es.execute_single(100,1)
    print(ind_best)
    data_ind = ([ind_iter,ind_fit,nd_sigma])
    draw_individual(data_ind) 

if __name__ == '__main__':

    execute_for_ind()
    
    #execute_for_avg()

    
