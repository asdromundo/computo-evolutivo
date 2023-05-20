#math.exp(x)
#math.sqrt(x)
#math.e
import math 
import numpy as np

def ackley(vector): 

	n = len(vector)
	sum_sq_term = np.sum(np.square(vector))
	cos_term = np.sum(np.cos(2 * math.pi * vector))
	term1 = -20.0 * math.exp(-0.2 * math.sqrt((1.0/n) * sum_sq_term))
	term2 = -math.exp((1.0/n) * cos_term)
	term3 = 20.0 + math.e

	return term1 + term2 + term3

