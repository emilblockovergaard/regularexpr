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


    def __init__(self):
        variable_ref = None

    def print_expr_type(self):
        print("Im a undefined expr!")

    def evaluate(self):
        return variable_dict[self.var_as_str]
        #return self.var_ref

    def add_child(self, child):
        if isinstance(self, NotExpr):
            print("adding child to not-expr")
            print(child)
        if self.l_child is None:
            self.l_child = child
            return True

        if isinstance(self, OrExpr) or isinstance(self, AndExpr):
            if self.r_child is None:
                self.r_child = child
                return True

        # If the current node is full we try to add to the left child
        return self.l_child.add_child(child)


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

        print(str(type(self))[17:-2], end="  ")
        print(self.var_as_str)

        if self.l_child is not None and isinstance(self, NotExpr):
            self.l_child.print_tree(depth+1, 3)
        elif self.l_child is not None:
            self.l_child.print_tree(depth + 1, 1)
        if isinstance(self, OrExpr) or isinstance(self, AndExpr):
            if self.r_child is not None:
                self.r_child.print_tree(depth + 1, 2)



class OrExpr(Expr):
    r_child = None
    def print_expr_type(self):
        print("Im an OR expr!")

    def evaluate(self):
        return self.r_child.evaluate() or self.l_child.evaluate()


class AndExpr(Expr):
    r_child = None
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

    def add_child(self, child):
        if self.l_child is None:
            self.l_child = child
            return True
        else:
            print("cant add to NOT, it's full!, tried to add: ", end="")
            print(child, end=" of type ")
            print(str(type(child))[17:-2])

            return False

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


# Creates a OR-tree based on a list of heads, these heads should be of, but not limited to, type Expr or NotExpr
def create_or_head(or_list):
    print("Generating OR tree from list!")
    while len(or_list) >= 2:
        new_or_node = OrExpr()
        new_or_node.add_child(or_list[0])
        or_list.pop(0)
        new_or_node.add_child(or_list[0])
        or_list.pop(0)
        or_list.append(new_or_node)
    return or_list[0]


def create_not_expr(start_node, list_in):
    child = Expr()
    child.var_as_str = list_in[0][1]
    list_in.pop(0)
    start_node.add_child(child)

def generate_and_tree(and_list_in):
    tree_head = AndExpr()

    print(and_list_in)
    while len(and_list_in)> 1:
        print("Combining an AND pair")
        combined = AndExpr()
        combined.add_child(and_list_in[0])
        combined.add_child(and_list_in[1])
        and_list_in.pop(0)
        and_list_in.pop(0)
        and_list_in.append(combined)
    else:
        print("Only 2 or less nodes!")
    print(and_list_in)

    return and_list_in[0]

def string_to_node(string_in):
    #if the element is a NOT we create child's accordingly
    if string_in[0] == '~':
        print("It's a NOT expr!")
        new_head = NotExpr()
        new_var_expr = Expr()
        new_var_expr.var_as_str = string_in[1:]
        new_head.add_child(new_var_expr)
    else:
        new_head = Expr()
        new_head.var_as_str = string_in[0:]
    return new_head

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    belief_base = []
    variable_dict = {}
    variables = VarTable()
    # First we try to implement expression: "(A&B)|C" into our code simply being able to represent it
    # Then we might add how to input a expression
    # Then we can add revision and stuff

    # Base = {(A|B),(~A&~B)}

    str_in = input("Input a belief in CN-Form (make sure it's valid!): ")
    #str_in = "(A|B|C) & ~D" # Remove this
    #str_in = "(A|B|C) & (D<<G & D >>G)" # Remove this
    str_in = "(A|B|C|D) & G & K & P & ~L & ~M, A | B" # Remove this
    #str_in = "C & (B | ~C)" # Remove this
    str_in = str(convert_print_to_cnf(str_in))
    str_cpy = str_in
    str_in = remove_exess(str_in)
    print(str_cpy)
    print(str_in)

    # Add all variable names to a dictionary
    test_str = str_in.replace(",","").replace("&","").replace("|","")
    print(test_str)
    i=0
    while i < len(test_str):
        if test_str[i] == '~':
            print("it's a not")
            i+=1
            print(test_str[i])
            variable_dict[test_str[i]] = False
        else:
            variable_dict[test_str[i]] = True
        i +=1

    print(variable_dict)
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

    beliefs = str_in.split(",")
    print(beliefs)
    print("there's " + str(len(beliefs)) + " beliefs")
    while len(beliefs) > 0:
        andElems = list(beliefs[0].split("&")) # Create array of elements separated by AND's
        beliefs.pop(0)
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
        and_heads = []
        print("Printing or-elems: ", end="")
        print(orElems)
        print("\nGenerating nodes: ")

        # Loop through the list of lists
        for x in orElems:

            # If it only contains one member we create a node from this:
            if len(x) == 1:
                # Add to the list of and heads
                and_heads.append(string_to_node(x[0]))

            # Otherwise we can see it's a or list:
            else:
                or_heads = []
                for k in x:
                    # Add to the smaller list of Or heads that will be combined afterwards:
                    or_heads.append(string_to_node(k))

                # Combine the or_list and add the generated head to the and_list:
                and_heads.append(create_or_head(or_heads))


        # for x in orElems:
        #     print(x)
        #     if x[0][0]== '~':
        #         print("It's a NOT expr!")
        #         not_head = NotExpr()
        #         create_not_expr(not_head, x)
        #         and_head.add_child(not_head)
        #         and_heads.append(not_head)
        #     else:
        #         if len(x) == 1:
        #             print("It's a single expression!")
        #             new_expr = Expr()
        #             new_expr.var_as_str = x[0]
        #             x.pop(0)
        #             and_heads.append(new_expr)
        #         else:
        #             print("It's a OR expr!")
        #             or_head = OrExpr()
        #             create_or_expr(or_head, x)
        #             or_head.print_tree(False)
        #             and_head.add_child(or_head)
        #             and_heads.append(or_head)

        print(orElems)

        print("\n\nPrinting and_heads: ")
        total_tree = generate_and_tree(and_heads)
        total_tree.print_tree()
        belief_base.append(total_tree)

    print(variable_dict)
    for i in range(0, len(belief_base)):
        print("Testing the " + str(i) + "th belief: " + str(belief_base[i].evaluate()))

    ### TODO 1.  Ask for a contradicting belief. 2. Let the user input a belief, which they know is true.
    ### TODO 4. Optain a checkSeq that checks a sequence of elements, throghout the variable dict.

    usr_choice = input("Enter a possiblity to do: \n Press r to enter a truth statement for revision ")
    if usr_choice == "r":
        usr_input_truth = input("Enter a truth statement on the form of Literal, True/False:\n Example: G,False: \n")
    usr_input_truth_list = usr_input_truth.split(",")
    variable = usr_input_truth_list[0]
    variable_boolean = None
    if usr_input_truth_list[1].lower().strip() == "false":
        variable_boolean = False
    elif usr_input_truth_list[1].lower().strip() == "true":
        variable_boolean = True
    print(variable_boolean)
    #Dictionary of set, to test from
    checkDict = {}
    #input the name of the variable and the truth value from user input to a dictionary for checking with the existing dictionary.
    checkDict.update({variable,variable_boolean})
    print(checkDict)








    # print("Left par: %d \t Right par: %d" % (first_right, first_left))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
