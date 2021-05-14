# TODO Fix med resten af MAIN.py
from sympy.logic.boolalg import to_cnf
from sympy.abc import A, B, D
import numpy as np

#Methods
def convertAndPrintCNF(expr_inpt):
    expr_inpt = expr_inpt.split(",")
    CNF_array = []
    for i in range(0, len(expr_inpt)):
        CNF_array.append(to_cnf(expr_inpt[i]))
    print(CNF_array)
    return CNF_array

def revision(bb, r):
    #TODO
    # Perform revision, checking with contradiction etc for each element of the subarray of CNFS
    # Use the main.py script to perform the checking. Each value for each statement there is based on either 0 | 1.

    for i in range(0, len(input)):
        i = []

    return i





# First step, convert to CNF
expr_inpt = input("Please enter an expression: \n")

action = input("Select an action: \n print: Prints the belief base \n revision: Performs revision on the belief base\n")
# Convert expression to CNF
if action == "print":
    CNF_Array = convertAndPrintCNF(expr_inpt)










# Second step #TODO

