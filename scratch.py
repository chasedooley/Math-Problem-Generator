import random
import itertools
import math

def get_coefficients(degree, lowbound=-10, highbound=10):
    """Creates randomized coefficients for expressions within a range,
    including fractions and integers, resulting in a list with degree+1 elements

    First element in list is always non-zero value
    
    Lowbound param should be lower than highbound param, but the function
    will correct for this if not"""

    def package(value1, value2=0): # packages the values into coeff list for the return
        sign = lambda x : '+' if x >= 0 else '-' # determines the sign of the coefficient
        if value2 == 0: # if value2 is 0, then the coefficient is a whole number integer
            return [sign(value1), abs(value1)] # splits sign of integer and the value for parsing later
        return [sign(value2), abs(value1), '/', abs(value2)]
    
    def create_coefficient(lowbound, highbound):
        # creates a sample of integers to pull from
        try:
            mean_value = round((abs(lowbound) + abs(highbound))/2)
            values = random.sample(range(lowbound, highbound), mean_value)
        except ValueError: # random.sample will raise ValueError is k (mean_value) is greater than the range
            print(f"Error: range too small, using {lowbound*5}, {highbound*5}")
            values = random.sample(range(lowbound*5, highbound*5), 5)

        # lambda function to get a random value from the values sample   
        get_value = lambda : values[random.randint(0, len(values)-1)]

        randval = random.randint(0, 4) # determines if coeff will be integer or fraction

        if randval > 1: # 60% favor to integers
            coeff = random.choice((get_value(), 0))
            return package(coeff)
        else:
            if randval == 0: # 20% for a 1/value fraction
                denom = get_value()
                while True: # prevents value/0 forms
                    if denom == 0:
                        denom = get_value()
                    else:
                        break
                if abs(denom) == 1:
                    return package(1)
                return package(1, denom)
            else: # 20% for value/value fraction
                numer = get_value()
                denom = get_value()
                while True: # prevents value/0 forms
                    if denom == 0:
                        denom = get_value()
                    else:
                        break
                if numer == 0: # prevents 0/value forms; returns 0 coeff
                    return package(0)
                elif abs(numer) == abs(denom): # prevents a/a value forms; returns 1
                    return package(1)
                else:
                    return package(numer, denom) # returns a/b form

    if lowbound > highbound:
        lowbound, highbound = highbound, lowbound

    coeffs = []
    for d in range(degree+1):
        coeff = create_coefficient(lowbound, highbound)
        if d == 0 and coeff[1] == 0: # prevent first element from being 0
            coeff[1] = 1
        coeffs.append(coeff)
    return coeffs

def get_nthroot(root, function=False, expression=None):
    """ Creates an nth-root expression, of either a coefficient or an expression"""
    if function:
        radicand = expression        
    elif random.randint(0, 2) >= 1 :
        radicand = expression        
    else:
        radicand = get_coefficients(0, 1, 10)

    coeff = get_coefficients(0, -10, 10)[0] # should return a single coefficient
    nthroot = str(root) + "-root"
    term = [coeff, nthroot, '(', radicand, ')']
    return term

def get_trigfunct(indeterminant, degree=1, inverse=False, hyperbolic=False, function=False, expression=None):

    """ Creates a trigonometric function, including inverse and hyperbolic forms, and can
        use an expression"""
    # Collections of the trigonometric and hyperbolic functions, and their inverses (arc-)
    trigs = ["sin", "cos", "tan", "csc", "cot", "sec"]
    arctrigs = ["arcsin", "arccos", "arctan", "arccsc", "arccot", "arcsec"]
    hypers = ["sinh", "cosh", "tanh", "csch", "coth", "sech"]
    archypers = ["arcsinh" "arccosh", "arctanh", "arccsch", "arccoth", "arcsech"]

    # A lambda function for getting a random function from a list above
    get_funct = lambda lst : lst[random.randrange(0, len(lst))]

    # Determining which list to pull from
    if inverse:
        if hyperbolic:
            funct = get_funct(archypers)
        else:
            funct = get_funct(arctrigs)
    else:
        if hyperbolic:
            funct = get_funct(hypers)
        else:
            funct = get_funct(trigs)

    # Determining what will go inside the function
    if function:
        inside = expression
    elif random.randint(0, 4) >= 2:
        inside = indeterminant
    else:
        inside = get_coefficients(0)

    coeff = get_coefficients(0, -10, 10)[0]

    return [coeff, funct, "**", degree, "(", inside, ")"]

def get_log(indeterminant=None, base=None, function=False, expression=None):
    
    # Determines the inside of the function
    if function:
        inside = expression
    elif indeterminant is not None:
        inside = indeterminant
    else:
        inside = random.randrange(0, 10)

    # Defaults to base e, the natural logarithm (ln)
    if base is not None:
        log = "log-" + str(base)
    else:
        log = "ln"
    
    coeff = get_coefficients(0, -10, 10)[0]
    return [coeff, log, '(', inside, ')']

def get_expon(indeterminant=None, function=False, expression=None):

    if function:
        exponent = expression
    elif indeterminant is not None:
        exponent = indeterminant
    else:
        exponent = random.randrange(0, 10)
    
    coeff = get_coefficients(0, -10, 10)[0]
    return [coeff, 'e**', exponent]


print(get_expon(function=True, expression='Polynomial'))