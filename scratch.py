import random
import itertools
import math

get_coefficient = lambda x, y: random.randint(x, y)

def get_nthroot(root):
    #get_nth = lambda : random.choices([random.randint(5, 10), 4, 3, 2], cum_weights=[5, 15, 35, 89])[0]
    
    if random.randint(0, 4) > 1:
        radicand = get_coefficient(1, 10)
    else:
        radicand = "Polynomial"

    coeff = get_coefficient(-10, 10)
    
    nthroot = str(root) + "-root"
    term = [coeff, nthroot, '(', radicand, ')']
    return term

print(get_nthroot(3))