Utilizado 

SO : ubuntu 20.04 
Python 3.8 
Biblioteca utilizada : pandas 

MINICONDA 
Se instaló la Biblioteca de pandas utilizando miniconda.
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


Ejecucion del programa : 

Estando en el directorio de la tarea '316032708', el script en donde se ejecutan los algoritmos es 
src/executable.py, el comando es 

    python3 src/executable.py x 

    Ejemplo : 

    python3 src/executable.py 0   -> es ejecutar recocido simulado con el ejemplar ejeL1n10.txt

Donde x va de 0 a 8 , los valores de x representan que ejemplar desear ejecutarse con recocido simulado 

    0 : ejeL1n10.txt
    1 : ejeL10n20.txt
    2 : ejeL14n45.txt
    3 : ejeknapPI_11_20_1000_100.txt
    4 : ejeknapPI_1_50_1000000_14.txt
    5 : ejeknapPI_3_200_1000_14.txt
    6 : ejeknapPI_13_100_1000_18.txt
    7 : eje1n1000.txt
    8 : eje2n1000.txt



