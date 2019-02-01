# author: Chase M. Dooley
# date: 30/01/2019
# description: this file contains the classes for each individual from of mathematical expressions, e.g. polynomial, algebraic, closeform, & mathematical
#              each class has certain functions and attributes unit to it


def problem_generator(expression, num_problems):
    """ A generator; generates randomized problems per attributes
        @expression: type of math expression to generate from
        @num_problems: number of problems to generate (will yield after each)"""