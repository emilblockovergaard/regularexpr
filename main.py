# This is a sample Python script.
from sympy.logic.boolalg import to_cnf
from sympy import *
from sympy.abc import A, B, D


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Sikre at expr virker korrekt
# Input, tjek det er korrekt

# Plausability table

# Consistency check
def convert_print_to_cnf(expr_inpt):
    expr_inpt = expr_inpt.split(",")
    CNF_array = []
    for i in range(0, len(expr_inpt)):
        CNF_array.append(to_cnf(expr_inpt[i]))
    return CNF_array


def remove_exess(in_str):
    in_str = in_str.replace("[", "")
    in_str = in_str.replace("(", "")
    in_str = in_str.replace(")", "")
    in_str = in_str.replace("]", "")
    in_str = in_str.replace(" ", "")
    return in_str


class Expr:
    var_ref = None  # Reference to variable
    var_as_str = ""
    l_child = None  # Children
    r_child = None

    def __init__(self):
        variable_ref = None

    def print_expr_type(self):
        print("Im a undefined expr!")

    def evaluate(self):
        return self.var_ref

    def add_child(self, child):
        if self.l_child is None:
            self.l_child = child
            return True

        if self.r_child is None:
            self.r_child = child
            return True

        self.l_child.add_child(child)
        return True

    def print_tree(self, depth, is_right=False):

        if self.l_child is not None:
            self.l_child.print_tree(depth + 1, False)
        if self.r_child is not None:
            self.r_child.print_tree(depth + 1, True)
        print("\t" * depth, end="")
        if is_right:
            print("R: ", end="")
        else:
            print("L: ", end="")
        print(self.var_as_str)


class OrExpr(Expr):
    def print_expr_type(self):
        print("Im an OR expr!")

    def evaluate(self):
        return self.r_child.evaluate() or self.l_child.evaluate()


class AndExpr(Expr):
    def print_expr_type(self):
        print("Im an AND expr!")

    def evaluate(self):
        if self.l_child is None or self.r_child is None:
            print("Error! AND doesnt have enough children to evaluate!")
            return False

        return self.r_child.evaluate() and self.l_child.evaluate()


class NotExpr(Expr):
    def print_expr_type(self):
        print("Im a NOT expr!")

    def evaluate(self):
        return not self.l_child.evaluate()


class VarClass:
    name_of_elem = ""
    value = True

    def __init__(self, name_in, val_in):
        self.name_of_elem = name_in
        self.value = val_in

    def to_string(self):
        return self.name_of_elem + ": " + str(self.value)

    def return_val(self):
        return self.value


class VarTable:
    def __init__(self):
        self.var_list = []

    def print_elems(self):
        print("Printing list: ", end="")
        for elem in self.var_list:
            print(elem.to_string()+", ", end="")
        print("")

    def add_elem(self, val_str):
        new_elem = None
        # print("adding element! " + val_str)
        if "~" in val_str:
            new_elem = VarClass(val_str[1], False)
        else:
            new_elem = VarClass(val_str, True)

        if len(self.var_list) == 0:
            print("Added element!")
            self.var_list.append(new_elem)
            return True

        for elem in self.var_list:
            if elem.name_of_elem == new_elem.name_of_elem:
                print("Element already exists!")
                return False
            else:
                print("Added element!")
                self.var_list.append(new_elem)
                return True

    # Returns value of element if not found return false
    def return_val_of_elem(self, name_str):
        for elem in self.var_list:
            if elem.name_of_elem == name_str:
                return elem.return_val()
            else:
                return False


class ParenPairs:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_index_in_pair(self, x):
        if self.right > x > self.left:
            return True
        else:
            return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    belief_base = []
    variables = VarTable()
    # First we try to implement expression: "(A&B)|C" into our code simply being able to represent it
    # Then we might add how to input a expression
    # Then we can add revision and stuff

    # Variables/table
    var_a = True
    var_b = False
    var_c = True

    my_and = AndExpr()

    and_left = Expr()
    and_left.var_ref = var_a

    and_right = Expr()
    and_right.var_ref = var_b

    my_and.add_child(and_left)
    my_and.add_child(and_right)

    my_or = OrExpr()

    left_1 = Expr()
    left_1.var_ref = var_c

    print("test")

    my_or.add_child(left_1)
    my_or.add_child(my_and)

    belief_base.append(my_or)

    for i in belief_base:
        print("Eval: " + str(i.evaluate()))

    # print("Eval2: "+ str(my_or.evaluate()))

    str_in = input("Input a belief in CN-Form: ")
    str_in = "~(A|B) & (C | D) & C"
    str_in = str(convert_print_to_cnf(str_in))
    str_in = remove_exess(str_in)
    print(str_in)
    # Find pairs of "(" and ")"
    # Test string: ((A&B)&(C|B))&(A|B)      CNF form ->     A & B & (C|B) & (A|B)
    # (A&B)&C -> A&B&C

    pair_list = []

    left_par = 0
    right_par = 0
    for chara in str_in:
        if chara == '(':
            left_par += 1
        if chara == ')':
            right_par += 1

    if left_par != right_par:
        print("Error in input not equal amount of parenthesis!")
    else:
        print("Left par: %d \t Right par: %d" % (left_par, right_par))


    andElems = str_in.split("&")
    orElems = []
    for x in range(0, len(andElems)):
        orElems.append(andElems[x].split("|"))

    for x in andElems:
        print("andlemes: " + str(x))
    variables.print_elems()
    for i in range(0, len(orElems)):
        #print("Subsub print: " + str(orElems[i]))
        for element in orElems[i]:
            print("variables: " + element)
            variables.add_elem(element)
    variables.print_elems()





    # print("Left par: %d \t Right par: %d" % (first_right, first_left))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
