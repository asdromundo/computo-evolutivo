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

//  d) Tenth Power Function
double tenth_power_function(double x[], int size) {
    double sum = 0;
    for (int i = 0; i < size; i++) {
        sum +=  pow(x[i],10);
    }
    cout << "Result: " << sum << endl;

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