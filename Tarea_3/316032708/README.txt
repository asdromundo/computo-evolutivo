Utilizado 

SO : ubuntu 22.04.04 
Python 3.10.9
Bibliotecas utilizadas : 
        - pandas 
        - numpy
        - matplotlib
        - scipy

Instrucciones para PANDA :
MINICONDA 
Se instaló la Biblioteca de pandas utilizando miniconda o puede instalarse con pip/pip3
Para instalar miniconda : 

    sudo apt update 

    sudo apt upgrade 

    wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh


Estando en el directorio donde se instalo el .sh :

    sh ./Miniconda3-py39_4.12.0-Linux-x86_64.sh

PANDAS 

    conda create -n name_of_my_env python

    source activate name_of_my_env

    conda install pandas

Instrucciones para NUMPY: 
    
    pip install numpy

Instrucciones para MATPLOTLIB 
Se intstala tanto con pip como con miniconda : 
    
    pip install matplotlib

    ó 

    conda install -c conda-forge matplotlib

Instrucciones para SCIPY 
Se instala con pip : 

    pip install scipy




Ejecucion del programa : 

Estando dentro del directorio de la tarea '316032708', el script en donde se ejecutan los algoritmos es src/executable.py y el comando es 

    python3 src/executable.py x:int y:int z:int w:int v:float 

Donde 
    x va de 0 a 4 : los valores de x representan que ejemplar desear ejecutarse con búsqueda local iterada 
        0 : ejeL14n45.txt
        1 : ejeknapPI_3_200_1000_14.txt
        2 : eje1n1000.txt
        3 : eje2n1000.txt
        4 : n_1000_c_1000000_g_6_f_0.3_eps_0.001_s_100.txt

    y : es el número de iteraciones para búsqueda local iterada 

    z : es el número de iteraciones para hill climbing   //De este modo el total de iteraciones es y * z

    w : es la estrategia a usar 
        0 : Perturbacion Aleatoria 
        1 : Perturbación Basada en Frecuencia 

    v : es la fuerza de perturbación que está en el intervalo (0,1) //El recomendado es entre .4-.5 

Ejemplo : 

    python3 src/executable.py 0 1000 5000 0 .4  -> 
es usando el ejemplar "ejeL14n45.txt (0)" , con 1000 iteraciones para búsqueda local iterativa, con 500 iteraciones para hill climbing, usando la estrategia de perturbacion aleatoria (0) y con fuerza de perturbacion .4 
Por defecto la temperatura establecida para el criterio de aceptacion es de 20 

Es IMPORTANTE resaltar, que NO SE PASA como parámetro el nombre del archivo para guardar la mejor solución encontrada ya que el nombre del archivo de salida tiene el mismo nombre que el archivo de data, sólo que éste se encuentra en la carpeta output/. Por ejemplo, para el anterior ejemplar "ejeL14n45.txt" el archivo donde se guarda la mejor solución encontrada es "output/ejeL14n45.txt". 

Adicionalmente en el script excecutable.py se encuentran algunas lineas comentadas que permiten la visualizacion de datos. 

ACERCA DE LA CARPETA OUTPUT : 

La carpeta 316032708/output contiene un archivo .txt por cada ejemplar en la carpeta 316032708/data, cada uno de estos archivos contiene informacion sobre la mejor solucion encontrada en una ejecucion del algoritmo ILS (tipicamente 1000 iteraciones para ils y 500 para hill climbing). En la carpeta 316032708/output/best_sols se encuentran (por cada ejemplar) los mejores valores objetivos encontrados en 10 repeticiones del algoritmos ILS usando ambas estrategias y fuerza de perturbacion .4, estos datos son los que se utilizaron para la visualizacion en las graficas y pueden ser generados de nuevo por medio de la funcion src/excecutable.py -> generate_avg_evol. 



