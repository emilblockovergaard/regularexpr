# This is a sample Python script.

from sympy import *

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
    in_str = in_str.replace("]", "")
    in_str = in_str.replace("(", "")
    in_str = in_str.replace(")", "")
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

    def print_tree(self, depth = 0, placement=0):
        print("\t" * depth, end="")
        if placement == 0:
            print("Head: ", end="")
        elif placement == 1:
            print("L: ", end="")
        elif placement == 2:
            print("R: ", end="")
        else:
            print("Not: ", end="")

        print(self.var_as_str)

        if self.l_child is not None and isinstance(self, NotExpr):
            self.l_child.print_tree(depth+1, 3)
        elif self.l_child is not None:
            self.l_child.print_tree(depth + 1, 1)
        if self.r_child is not None:
            self.r_child.print_tree(depth + 1, 2)



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

# Takes a list of strings, this list should be split by character '|'
def create_or_expr(start_node, or_list):
    if len(or_list) == 1:
        new_node = Expr()
        new_node.var_as_str = or_list[0]
        or_list.pop(0)
        return

    if len(or_list) > 2: # more than 2 elements in list?
        left_var = Expr()
        left_var.var_as_str = or_list[0]
        or_list.pop(0)
        start_node.l_child = left_var

        start_node.r_child = OrExpr()
        create_or_expr(start_node.r_child, or_list)
    else:
        left_var = Expr()
        left_var.var_as_str = or_list[0]
        or_list.pop(0)
        start_node.l_child = left_var

        right_var = Expr()
        right_var.var_as_str = or_list[0]
        or_list.pop(0)
        start_node.r_child = right_var


def create_not_expr(start_node, list_in):
    child = Expr()
    child.var_as_str = list_in[0][1]
    list_in.pop(0)
    start_node.add_child(child)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    belief_base = []
    variables = VarTable()
    # First we try to implement expression: "(A&B)|C" into our code simply being able to represent it
    # Then we might add how to input a expression
    # Then we can add revision and stuff



    str_in = input("Input a belief in CN-Form (make sure it's valid!): ")
    #str_in = "(A|B|C) & ~D" # Remove this
    str_in = "(A|B|C|D) & ~G" # Remove this
    str_in = str(convert_print_to_cnf(str_in))
    str_in = remove_exess(str_in)
    print(str_in)

    # Find pairs of "(" and ")"
    # Test string: ((A&B)&(C|B))&(A|B)      CNF form ->     A & B & (C|B) & (A|B)
    # (A&B)&C -> A&B&C
    #
    # pair_list = []
    #
    # left_par = 0
    # right_par = 0
    # for chara in str_in:
    #     if chara == '(':
    #         left_par += 1
    #     if chara == ')':
    #         right_par += 1
    #
    # if left_par != right_par:
    #     print("Error in input not equal amount of parenthesis!")
    # else:
    #     print("Left par: %d \t Right par: %d" % (left_par, right_par))



    andElems = list(str_in.split("&")) # Create array of elements separated by AND's
    orElems = []

    for x in range(0, len(andElems)):
        orElems.append(andElems[x].split("|"))

    # #variables.print_elems()
    # for i in range(0, len(orElems)):
    #     #print("Subsub print: " + str(orElems[i]))
    #     for element in orElems[i]:
    #         print("variables: " + element)
    #         #variables.add_elem(element)
    #
    # #variables.print_elems()

    # Create a tree from OR
    or_head = None
    not_head = None
    and_head = AndExpr()
    print("Printing or-elems: ", end="")
    print(orElems)
    print("\nPrinting or elems: ")
    for x in orElems:
        print(x)
        if x[0][0]== '~':
            print("It's a NOT expr!")
            not_head = NotExpr()
            create_not_expr(not_head, x)
            and_head.add_child(not_head)
        else:
            print("It's a OR expr!")
            or_head = OrExpr()
            create_or_expr(or_head, x)
            or_head.print_tree(False)
            and_head.add_child(or_head)

    print(orElems)

    and_head.print_tree()









    # print("Left par: %d \t Right par: %d" % (first_right, first_left))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
