# author: Chase M. Dooley
# date: 30/01/2019
# description: this file contains the classes for each individual form of mathematical expressions, e.g. polynomial, algebraic, closeform, & mathematical
#              each class has certain functions and attributes unit to it

import random, itertools

class Expression:
    
    def get_coefficients(self, degree, lowbound=-10, highbound=10):
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


    def get_nthroot(self, root, function=False, expression=None):
        """ Creates an nth-root expression, of either a coefficient or an expression"""
        if function:
            radicand = expression        
        elif random.randint(0, 2) >= 1 :
            radicand = expression        
        else:
            radicand = self.get_coefficients(0, 1, 10)

        coeff = self.get_coefficients(0, -10, 10)[0] # should return a single coefficient
        nthroot = str(root) + "-root"
        term = [coeff, nthroot, '(', radicand, ')']
        return term

class Polynomial(Expression):

    def __init__(self, degree=1, indeterminates='x', lowbound=-10, highbound=10):
        super()
        self.degree = degree
        self.indets = indeterminates
        self.lowbound = lowbound
        self.highbound = highbound
        self.__expression = []

        self.new()

    def __repr__(self):
        return f"Poloynomial(degree={self.degree}, lowbound={self.lowbound}, highbound={self.highbound})"

    def __call__(self):
        return self.__expression

    def new(self):

        """Creates a polynomial expression using the set attributes"""
        self.__expression = []
        coeffs = self.get_coefficients(self.degree)

        if self.degree == 0:
            self.__expression.append(coeffs)

        # a list of all combinations of the interdetermines (minus the empty set)
        indets_subset = []
        for v in range(0, len(self.indets)+1):
            for subset in itertools.combinations(self.indets, v):
                indets_subset.append(subset)
        indets_subset.pop(0)

        # gets a random subset if there's most than one; else returns the single subset
        def get_subset():
            if len(indets_subset) == 1:
                subset = indets_subset[0]
            else:
                index = random.randint(0, len(indets_subset)-1)
                subset = indets_subset[index]
                indets_subset.pop(index)
            return subset

        # randomly generates each subterm of the expression using the indeterminants and degrees
        def get_subterms():
            form = []
            subsets = []
            lens_subsets = 0
            # generates a random degree between 0 and degree (highest degree in expression)
            get_degree = lambda : random.randint(0, self.degree)
        
            # randomly selects the combination subsets of the indeterminants for the form of the expression
            # also calculates the total number of indeterminants, for use in calculating needed degrees
            for _ in range(self.degree):
                subset = get_subset()
                lens_subsets += len(subset)
                subsets.append(subset)
            
            # randomly generates the degrees needed for each indeterminant in the expression
            degrees = []
            for _ in range(lens_subsets):
                degrees.append(get_degree())

            # ensures the expression will have the passed degree
            if self.degree not in degrees:
                degrees.insert(0, self.degree)

            # combines the terms and the degrees into subterms
            degree_counter = 0
            for ss in subsets:
                term = []
                for i in range(len(ss)):
                    t = ss[i]
                    degr = degrees[degree_counter]
                    term.extend([t, "**", degr])
                    degree_counter += 1
                form.append(term)
            return form
        
        # builds the expression; combines the coeffs and the subterms
        self.__expression = list(zip(coeffs, get_subterms()))
        self.__expression.append(coeffs[-1]) # inputs the ending coefficient (the intercept)

    def random(self):
        """Generates a random expression using random degree and indeterminants"""
        self.degree = random.randint(1, 5)
        self.indets = random.choice(['x', 'xy', 'xyz', 'wxyz'])
        self.new()

class Algebraic(Expression):
    
    def __init__(self, degree=1, indeterminants='x', lowbound=-10, highbound=10, root=1, rational=True, proper=True):
        super()
        self.degree = degree
        self.indets = indeterminants
        self.lowbound = lowbound
        self.highbound = highbound
        self.root = root
        self.rational = rational
        self.proper = proper
        self.__expression = []
        """TODO: Consider that all of these variables belong under Expression, including Polynomial's variables"""
        self.new()

    def __repr__(self):
        return f"""Algebraic(degree={self.degree}, indeterminants={self.indets}, lowbound={self.lowbound},
            highbound={self.highbound}, rational={self.rational}, root={self.root})"""

    def __call__(self):
        return self.__expression

    def new(self):
        """Creates an algebraic expression using the set attributes"""
        self.__expression = []
        less_degree = lambda : random.randint(0, self.degree-1) if self.degree > 1 else 0

        # if self.rational is true, then the expression is a rational function
        # if self.proper is true, then it's a proper rational function; P(x)/Q(x) where P(x) < Q(x)
        if self.rational and self.proper:

            Q_funct = Polynomial(degree=self.degree, indeterminates=self.indets, 
                            lowbound=self.lowbound, highbound=self.highbound)
        
            # if root is greater than one, an nth-root will replace P_funct; it could be a value or Polynomial
            if self.root > 1:
                expr = Polynomial(degree=self.degree, indeterminates=self.indets, 
                            lowbound=self.lowbound, highbound=self.highbound)

                P_funct = self.get_nthroot(self.root, expression = expr())
                self.__expression = [P_funct, "/", Q_funct()]
            else:  
                P_funct = Polynomial(degree=less_degree(), indeterminates=self.indets, 
                                lowbound=self.lowbound, highbound=self.highbound)
                self.__expression = [P_funct(), "/", Q_funct()]

        # if self.proper is false, then it's an improper rational function; Q(x)/P(x) where P(x) < Q(x)
        elif self.rational and not self.proper:

            Q_funct = Polynomial(degree=self.degree, indeterminates=self.indets, 
                lowbound=self.lowbound, highbound=self.highbound)
            
            # if root is greater than one, an nth-root will replace P_funct; it could be a value or Polynomial
            if self.root > 1:
                expr = Polynomial(degree=self.degree, indeterminates=self.indets, 
                            lowbound=self.lowbound, highbound=self.highbound)
                P_funct = self.get_nthroot(self.root, expression=expr())
                self.__expression = [Q_funct(), "/", P_funct]
            else:  
                P_funct = Polynomial(degree=less_degree(), indeterminates=self.indets, 
                                lowbound=self.lowbound, highbound=self.highbound)
                self.__expression = [Q_funct(), "/", P_funct()]

        else:
            # if root is greater than one, an nth-root will replace P_funct; it could be a value or Polynomial
            Q_funct = Polynomial(degree=self.degree, indeterminates=self.indets, 
                lowbound=self.lowbound, highbound=self.highbound)
            
            self.__expression = self.get_nthroot(self.root, function=True, expression=Q_funct())

    def random(self):
        """Generates a random expression using random attributes"""
        self.degree = random.randint(1, 5)
        self.root = random.choices([random.randint(5, 10), 4, 3, 2], cum_weights=[5, 15, 35, 89])[0]
        self.indets = random.choice(['x', 'xy', 'xyz', 'wxyz'])
        self.new()

class Closeform(Expression):
    """ Trigonometric, logarithmic functions"""
    pass

class Mathematical(Expression):
    """TODO: What is this really? Limit, derivative, and integral functions can all be 
    generated using the main program as a problem itself; is this for infinite series?"""
    pass


exp = Algebraic()
exp.random()
print(exp())