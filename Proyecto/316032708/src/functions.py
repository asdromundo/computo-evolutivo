#math.exp(x)
#math.sqrt(x)
#math.e
import math 
import numpy as np

def ackley(vector): 

	first_sum = 20*math.exp((math.sqrt((sum([x*x for x in vector]))/2))*(-0.2))

	second_sum = math.exp((sum([math.cos(2*math.pi*x) for x in vector]))/2)

	return 20 + math.e - first_sum - second_sum  

