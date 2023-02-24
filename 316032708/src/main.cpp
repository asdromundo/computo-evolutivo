#include <iostream>
#include <math.h>
#define _USE_MATH_DEFINES // for C++
#include <cmath>
                                                             
                     
using namespace std;

//  a) Sphere
double sphere_function(double x[], int size) {
    double sum = 0;
    for (int i = 0; i < size; i++) {
            sum += x[i] * x[i];
        
    }

    cout << "Result: " << sum << endl;

    return sum;
}

//  b) Ackley
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
    
    cout << result << endl;

    return  result; 
     
}

//  d) Tenth Power 
double tenth_power_function(double x[], int size) {
    double sum = 0;
    for (int i = 0; i < size; i++) {
        sum +=  pow(x[i],10);
    }
    cout << "Result: " << sum << endl;

    return sum;
}

//  e) Rastring
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
    
    cout << result << endl;

    return  result; 
     
}



int main()
{
    int vector[5] = {1,2,3,4}; 
    double vector_d[5] = {-3.2,-1.5,0.9,1.3,4.1}; 
    
    //print_array(vector,4); 
    rastrigin_funtion(vector_d, 5); 
    sphere_function(vector_d, 5 );

}