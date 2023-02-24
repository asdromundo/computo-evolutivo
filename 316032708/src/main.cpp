#include <iostream>
#include <math.h>
#include <string>
#define _USE_MATH_DEFINES // for C++
#include <cmath>
                                                             
                     
using namespace std;

//  a) Sphere
double sphere_function(double x[], int size) {
    double sum = 0;
    for (int i = 0; i < size; i++) {
            sum += x[i] * x[i];
        
    }

    return sum;
}

// # b) Ackley
double ackley_funtion(double vector[], int size){

    //Using M_E = e and M_PI=pi

    // This is the sum which has a square root 
    double first_sum = 0.0; 
    // This is the sum which has a cos 
    double second_sum = 0.0; 

    //First sum 
    for (int i=0; i < size; i++){
        first_sum += vector[i]*vector[i]; 
    }
    first_sum = first_sum/size;
    first_sum = sqrt(first_sum);
    first_sum = first_sum * (-0.2);
    first_sum = exp(first_sum); 
    first_sum = first_sum*20;  

    //Second Sum 
    for (int i=0; i < size; i++){

        second_sum += cos(2*M_PI*vector[i]); 
    }
    second_sum = second_sum/size; 
    second_sum = exp(second_sum);

    //Final return
    double result = 20+M_E-first_sum-second_sum;  

    return result; 
     
}

// # c) Grienwank
double griewank_funtion(double X[], int dimention){

    double sum = 0;
    double prod = 1;

    for (int i=0; i < dimention; i++){
        sum += (pow(X[i], 2)/4000);
        prod *= cos(double(X[i])) / sqrt(i+1);
    }

    return 1 + sum - prod;
}

//  d) Tenth Power Function
double tenth_power_function(double x[], int size) {
    double sum = 0;
    for (int i = 0; i < size; i++) {
        sum +=  pow(x[i],10);
    }

    return sum;
}

// # e) Rastring
double rastrigin_funtion(double vector[], int size){

    //Using M_E = e and M_PI=pi

    // This is the sum which has a square root 
    double first_sum = 10*size; 
    // This is the sum which has a cos 
    double second_sum = 0.0; 

    //First sum 
    for (int i=0; i < size; i++){
        first_sum += vector[i]*vector[i] - 10*(cos(2*M_PI*vector[i])); 
    }
    
    //Final return
    double result = first_sum+second_sum;  

    return result; 
     
}

// # f) Rosenbrock Function
double rosenbrock_function(double X[], int dimention){
    double sum;
    for (int i = 1; i < dimention-1; i++){
        sum += (100 * (X[i+1]-pow(X[i], 2))) + pow(1-X[i], 2);
    }
    return sum;
}

//ESQUEMA DE CODIFICACION 

/*
Funcion para obtener la precision dado el tamanio (numero de bits para el esquema) y el max,
en este caso nuestro intervalos son simetricos, por lo que sólo consideramos uno de ellos 
*/
double getPrecision(int size, double max){
    //Vamos a considerar 
    return max/(pow(2,size-1)-1); 

}

//Nuestro esquema es de 16 
bitset<16> doubleToBits(double num, double max){

    int halfRepresentation = round(num/getPrecision(16,max)); 
    bitset<16> schema(halfRepresentation);

    return schema; 

}

//CODIFICACION 
bitset<16> doubleToBinary(double num, double max){

    int halfRepresentation = round(num/getPrecision(16,max)); 
    bitset<16> schema(halfRepresentation);

    return schema; 

}

//DECODIFICACION 
double binaryToDouble(bitset<16> schema, double max){

    string var  = schema.to_string(); 
    //Falta generar bitset de 15  

    int halfRepresentation = schema.to_ulong(); 
    double precision = getPrecision(16,max); 

    return halfRepresentation*precision; 
}



int main()
{
    int vector[5] = {1,2,3,4}; 
    double vector_d[5] = {-3.2,-1.5,0.9,1.3,4.1}; 
    
    cout << "Sphere: " << sphere_function(vector_d, 5) << endl;
    cout << "Ackley: " << ackley_funtion(vector_d, 5) << endl;
    cout << "Griewank: " << griewank_funtion(vector_d, 5) << endl;
    cout << "Tenth Power: " << tenth_power_function(vector_d, 5) << endl;
    cout << "Rastrigin: " << rastrigin_funtion(vector_d, 5) << endl; 
    cout << "Rosenbrock: " << rosenbrock_function(vector_d, 5) << endl; 
    //Convierte -3.2 a binario en el rango de [-5.2, 5.2]
   bitset<16> binary = doubleToBits(3.2, 5.12); 

   cout << binary << endl;  

   cout << binaryToDouble(binary, 5.12) << endl; 

}


