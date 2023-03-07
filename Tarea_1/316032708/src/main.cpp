#include <iostream>
#include <iomanip>
#include "binoptimization"
#include "binary"


int main()
{
    const int dimention = 5;
    double vector_d[dimention] = {-3.2,-1.5,0,1.3,4.1};
    double interval = 2<<4;
    binary vector_bin;
    vector_bin = vector_to_single_binary(vector_d, dimention, interval, 4);
    std::cout << vector_bin << std::endl;
    std::cout << "Sphere: " << sphere(vector_bin, 5) << std::endl;
    std::cout << "Ackley: " << ackley(vector_bin, 5) << std::endl;
    std::cout << "Griewank: " << griewank(vector_bin, 5) << std::endl;
    std::cout << "Tenth Power: " << tenth_power(vector_bin, 5) << std::endl;
    std::cout << "Rastrigin: " << rastrigin(vector_bin, 5) << std::endl; 
    std::cout << "Rosenbrock: " << rosenbrock(vector_bin, 5) << std::endl; 
    
    //Convierte -3.2 a binario en el rango de [-5.2, 5.2]

    binary bin = double_to_binary(-0.1, interval); 
    std::cout << bin << std::endl;  
    std::cout << binaryToDouble(bin, interval) << std::endl; 

}
