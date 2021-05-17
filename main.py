
# Belief revision assignment implementation

import sys
import time

from sympy import *

def convert_print_to_cnf(expr_inpt):
    expr_inpt = expr_inpt.split(",")
    CNF_array = []
    for i in range(0, len(expr_inpt)):
        CNF_array.append(to_cnf(expr_inpt[i]))
    return CNF_array

def str_to_cnf_str(string_in):
    return str(to_cnf(string_in)).strip()

def remove_exess(in_str):
    in_str = in_str.replace("[", "")
    in_str = in_str.replace("]", "")
    in_str = in_str.replace("(", "")
    in_str = in_str.replace(")", "")
    in_str = in_str.replace("{", "")
    in_str = in_str.replace("}", "")
    in_str = in_str.replace(" ", "")
    return in_str

def total_strip_for_dict(string_in):
    return remove_exess(string_in).replace("~","").replace("&","").replace("|","").replace(",","")

class Expr:
    var_ref = None  # Reference to variable
    var_as_str = ""
    l_child = None  # Children


    def __init__(self):
        variable_ref = None

    def print_expr_type(self):
        print("Im a undefined expr!")

    def evaluate(self):
        return variable_dictionary[self.var_as_str]
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
            print("Child: ", end="")

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

# Generates an and tree from a list of things that should be "AND'ed", the list should contain nodes of type Expr or subclasses
def generate_and_tree(and_list_in):
    tree_head = AndExpr()

    #print(and_list_in)
    while len(and_list_in)> 1:
        #print("Combining an AND pair")
        combined = AndExpr()
        combined.add_child(and_list_in[0])
        combined.add_child(and_list_in[1])
        and_list_in.pop(0)
        and_list_in.pop(0)
        and_list_in.append(combined)

    #print(and_list_in)

    return and_list_in[0]

# Creates a Expr node or a NotExpr based on the string_in, this is used at the bottom when generating a tree
def var_str_to_expr(string_in):
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

# Tests a tree with a certain world
def test_tree(start_node, world_state):
    global variable_dictionary
    temp_dict = variable_dictionary

    variable_dictionary = world_state
    return_val = start_node.evaluate()
    variable_dictionary = temp_dict
    return return_val

# Returns true if the whole belief-list evaluates to true otherwise return False
def test_belief(belief_list):
    for index in range(0, len(belief_list)):
        if not belief_list[index].evaluate():
            return False
    return True

# Test/find a world where the belief base is possible
def find_worlds(dict_in):
    print(len(dict_in.keys()))

    #variable_dictionary["C"] = False
    #variable_dictionary["B"] = False
    variable_dictionary_copy = dict_in.copy()


    # Generate 2^N dictionaries.
    worlds = []
    number = 0
    key_list = list(dict_in.keys())
    print(key_list)
    for x1 in range(0, 2**len(dict_in)):
        worlds.append(dict_in.copy())
        #print(format(number, '04b'))

        for n in range(0,len(key_list)):
            if number & (1 << n):
                #print("True at: " + str(number & (1 << n)))
                worlds[x1][key_list[n]] = True
            else:
                worlds[x1][key_list[n]] = False
        number += 1

    print("\nAll possible worlds based on the variables:")
    print(worlds)

    # Now test each world and add valid worlds to a list
    valid_worlds = []
    for x1 in range(0, len(worlds)):
        global variable_dictionary
        variable_dictionary = worlds[x1]
        #print(variable_dictionary)
        #print("Testing world " + str(x1) + " : " + str(test_belief(belief_base)))
        if test_belief(belief_base):
            valid_worlds.append(worlds[x1])
    print("\nValid worlds:")
    print(valid_worlds)

def generate_all_valid_worlds(node, print_things = False):

    global variable_dictionary
    temp_dict = variable_dictionary

    # Generate 2^N dictionaries.
    worlds = []
    number = 0
    key_list = list(variable_dictionary.keys())
    if print_things: print("Key list: " + str(key_list))
    for x1 in range(0, 2**len(variable_dictionary)):
        worlds.append(variable_dictionary.copy())
        #print(format(number, '04b'))

        for n in range(0,len(key_list)):
            if number & (1 << n):
                #print("True at: " + str(number & (1 << n)))
                worlds[x1][key_list[n]] = True
            else:
                worlds[x1][key_list[n]] = False
        number += 1

    if print_things: print("\nAll possible worlds based on the variables:")
    if print_things: print(worlds)

    # Now test each world and add valid worlds to a list
    valid_worlds = []
    for x1 in range(0, len(worlds)):
        #print(variable_dictionary)
        #print("Testing world " + str(x1) + " : " + str(test_belief(belief_base)))
        if test_tree(node, worlds[x1]):
            valid_worlds.append(worlds[x1])
    if print_things: print("\nValid worlds:")
    if print_things: print(valid_worlds)

    return valid_worlds

# Takes 2 args, one is the node we should split into clauses, the second is the list it should be stored into, stores heads in the list
def generate_and_list(start_node, list_to_append_to):
    if not isinstance(start_node, AndExpr):
        list_to_append_to.append(start_node)
        return

    if start_node.l_child is not None:
        print("going to left child")
        generate_and_list(start_node.l_child, list_to_append_to)
    if isinstance(start_node, AndExpr) or isinstance(start_node, OrExpr):
        print("going to right child")
        if start_node.r_child is not None: generate_and_list(start_node.r_child, list_to_append_to)

def generate_list_split_and(start_node, compare_dict, and_list):
    # create a list for checking
    generate_and_list(start_node, and_list)
    print("Printing clauses:")
    for elem in and_list:
        print(elem.print_tree(),end="\n\n")

    for elem in and_list:
        while False:
            print("")

    if isinstance(start_node, OrExpr) or isinstance(start_node, AndExpr):
        if not(isinstance(start_node.l_child, OrExpr) or isinstance(start_node.l_child, AndExpr)):
            # we can check left child's key/
            print("tada")


class BeliefBase:
    list_of_beliefs = []

    def __init__(self):
        pass

    def update_var_dict(self):
        global variable_dictionary
        variable_dictionary.clear()
        for elem in self.list_of_beliefs:
            for char in total_strip_for_dict(elem.cnf_string):
                variable_dictionary[char] = False

    def print_base_strings(self):
        print("Printing belief base in strings:")
        for elem in self.list_of_beliefs:
            print("\t" + str_to_cnf_str(elem.cnf_string) + ",")

    def print_base_trees(self):
        print("Printing belief base in tree:")
        for elem in self.list_of_beliefs:
            elem.cnf_tree.print_tree()
            print("")

    def expand_base(self, cnf_string_in):
        for elem in self.list_of_beliefs:
            if convert_print_to_cnf(elem.cnf_string) == convert_print_to_cnf(cnf_string_in):
                print("Tried to add: "+ cnf_string_in +", belief already exists!")
                return False
        print("Adding: " + str(cnf_string_in))
        self.list_of_beliefs.append(BeliefNode(str(cnf_string_in)))
        return True

    def contract_base(self, cnf_string_in):
        for elem in self.list_of_beliefs:
            if str_to_cnf_str(elem.cnf_string) == str_to_cnf_str(cnf_string_in):
                self.list_of_beliefs.remove(elem)
                print("Removed element: " + str(cnf_string_in))
                return True
        print("Tried to remove: " + cnf_string_in +", couldn't find element!")
        return False

    def evaluate_all(self, print_each = False):
        global variable_dictionary
        print("Evaluating based on this state: " + str(variable_dictionary))
        return_val = True
        # Go through the list
        for elem in self.list_of_beliefs:
            # If one of the belief doesn't evaluate to true within the current state/world we return false
            if not elem.cnf_tree.evaluate():
                return_val = False

            if print_each:
                print("\t"+str(elem.cnf_tree.evaluate()))

        # We return true if we get through all the beliefs
        return return_val

    # NOT DONE!
    def check_for_contradictions(self, new_belief_node):
        # Divide belief base into clauses
        # Get valid worlds for each clause
        # Get new belief from user
        # Generate worlds for the new belief

        # Compare the worlds, check that one of the worlds from a clause also evals to true in the new belief
        # if not we have a contradiction.. i think

        clause_list = []#nothing
        for elem in self.list_of_beliefs:#nothing
            generate_and_list(elem.cnf_tree, clause_list) #nothing

        print("Clause-list: " + str(clause_list))

        new_belief_worlds = generate_all_valid_worlds(new_belief_node)

        print("New_belief_worlds: " + str(new_belief_worlds))

        clause_worlds = [] #nothing
        for elem in self.list_of_beliefs:
            clause_worlds.append(generate_all_valid_worlds(elem.cnf_tree))

        print("Clause_worlds: " + str(clause_worlds))

        # Create a list with a element for each belief
        test_val = []
        for elem in clause_worlds:
            test_val.append(False)

        for elem1 in range(0,len(clause_worlds)): # list of belief set worlds
            for elem2 in clause_worlds[elem1]: # loop through the lists in belief-set worlds

                for elem3 in new_belief_worlds: # the new knowledge
                    if elem2 == elem3: # if a world matches we set it to True
                        test_val[elem1] = True

        print("Is the belief allowed to stay?: " + str(test_val))
        return test_val

    # Remove all beliefs and insert the new one.
    def lazy_revision(self, string_in):
        self.list_of_beliefs.clear()
        global variable_dictionary
        variable_dictionary.clear()
        str_cpy = remove_exess(string_in).replace("~","").replace(",","").replace("&","").replace("|","")
        for x in str_cpy:
            variable_dictionary[x] = False
        self.expand_base(string_in)

class BeliefNode:
    cnf_string = ""
    cnf_tree = None

    # Input a raw string
    def __init__(self, string_in):
        self.cnf_string = string_in
        self.cnf_tree = create_tree_from_string(string_in)

    def print_string(self):
        print(self.cnf_string)

    def print_the_tree(self):
        self.cnf_tree.print_tree()

    def update_string_from_tree(self):
        cnf_string = "fuck"

# NOT DONE!
def string_from_tree(start_expr_node, out_str):
    # If normal expression:
    if not(isinstance(start_expr_node, OrExpr) or isinstance(start_expr_node, AndExpr) or isinstance(start_expr_node, NotExpr)):
        out_str += start_expr_node.var_as_str

# Takes a non-stripped string in CN-Form and creates a tree based on this, returns the head to the tree
def create_tree_from_string(string_in_raw):
    string_in = remove_exess(string_in_raw)
    and_elements = list(string_in.split("&")) # Create array of elements separated by AND's
    or_elements = []

    #Create list of lists
    for x in range(0, len(and_elements)):
        or_elements.append(and_elements[x].split("|"))

    # Create a tree from OR
    and_heads = []
    #print("Printing or-elems: ", end="")
    #print(or_elements)
    #print("\nGenerating nodes: ")

    # Loop through the list of lists
    for x in or_elements:
        # If it only contains one member we create a node from this:
        if len(x) == 1:
            # Add to the list of and heads
            and_heads.append(var_str_to_expr(x[0]))

        # Otherwise we can see it's a OR-list:
        else:
            or_heads = []
            for k in x:
                # Add to the smaller list of Or heads that will be combined afterwards:
                or_heads.append(var_str_to_expr(k))

            # Combine the or_list and add the generated head to the and_list:
            and_heads.append(create_or_head(or_heads))

    #print(or_elements)

    #print("\n\nPrinting and_heads and the generated tree: ")
    total_tree = generate_and_tree(and_heads)
    #total_tree.print_tree()
    return total_tree

def print_welcome_msg():
    str_to_print = "\n*********************************************************************************************************\n"
    str_to_print += "Welcome to our belief revision agent!\nThis program allows you to enter beliefs into a belief-base, "
    str_to_print += "the base will then updated correctly.\n\nThe format of input's should be as follows:\n\t1. Variables/literals should be "
    str_to_print += "single letters.\n\t\t- The program is case-sensitive so \"A != a\".\n\t2. You can't use the letter E as a variable/literal name.\n\t3. Logical operators such as AND, OR and others are written this way:\n\t\t- AND: \"&\""
    str_to_print += "\n\t\t- OR: \"|\"\n\t\t- NOT: \"~\"\n\t\t- IMPLICATION: \">>\" or \"<<\"\n\t\t- BI-IMPLICATION: \"(x >> y) & (y >> x)\""
    str_to_print += "\n\nEnjoy!\n\n*********************************************************************************************************\n"
    print(str_to_print)

if __name__ == '__main__':

    belief_base = BeliefBase()
    global variable_dictionary
    variable_dictionary = {}

    print_welcome_msg()

    str_in = input("Input a non contradicting belief: ")
    str_in = "a | e" # Remove this
    # str_in = "{(~r | p | s) & (~p | r) & (~s | r) & ~r}, {a | b},f & d"


    # Strip and convert the user input to a CNF string
    print("Test: " + str_to_cnf_str(str_in))
    str_in = str(convert_print_to_cnf(str_in)).replace("[","").replace("]","").replace("{","").replace("}","")
    print(str_in)

    # Add all variable names to a dictionary
    test_str = remove_exess(str_in).replace(",","").replace("&","").replace("|","")
    print(test_str)
    i=0
    while i < len(test_str):
        if test_str[i] == '~':
            i+=1
            variable_dictionary[test_str[i]] = False
        else:
            variable_dictionary[test_str[i]] = True
        i +=1

    print(variable_dictionary)

    # Split the string, so that we can have multiple beliefs at once
    beliefs = str_in.split(", ")
    print(beliefs)
    print("there's " + str(len(beliefs)) + " beliefs")

    # Add to the belief base
    while len(beliefs) > 0:
        belief_base.expand_base(str_to_cnf_str(beliefs[0]))
        beliefs.pop(0)

    belief_base.print_base_strings()

    #belief_base.contract_base(str_to_cnf_str("a | b"))
    #belief_base.print_base_strings()

    #belief_base.expand_base(str_to_cnf_str("a & b"))
    #belief_base.print_base_strings()

    #belief_base.expand_base(str_to_cnf_str("a & b"))
    #belief_base.print_base_strings()

    # Change all values to False
    variable_dictionary = dict.fromkeys(variable_dictionary, False)

    # belief_base.expand_base(str_to_cnf_str("~b"))

    print(belief_base.evaluate_all(True))

    #belief_base.lazy_revision(str_to_cnf_str("(c | d) & a"))

    generate_all_valid_worlds(belief_base.list_of_beliefs[0].cnf_tree)
    belief_base.print_base_strings()
    new_belief = BeliefNode("~a")
    belief_base.check_for_contradictions(new_belief.cnf_tree)

    time.sleep(0.1)
    sys.exit("Stopped on purpose")

    print(variable_dictionary)
    print(belief_base[0].evaluate())
    print("Changing A and B")
    variable_dictionary['A'] = False
    variable_dictionary['B'] = False
    print(belief_base[0].evaluate())
    find_worlds(variable_dictionary)
    # Go through tree
    # When at normal expression check if it contradicts the new check base
    check_dict = {'p': False}

    new_knowledge = input("Input a newly gained knowledge: ")
    converted = convert_print_to_cnf(new_knowledge)
    print(converted)
    # Generate a tree from this new line

    new_list = []
    generate_list_split_and(belief_base[0], check_dict, new_list)

    dict_list = []


# TODO:
#   a while loop where user can input 4 letters  "r, c, e, p"
#       r: will revise the base with a belief
#       c: contract a belief from the base
#       e: will expand the base with a belief
#       p: will print the base
#   revision, a system where adding a new belief also changes the current beliefs
#       resolution algorithm
#           perhaps a method could be similar to 1:24:00 in lecture 8
#
# New idea for Resolution algorithm:
#   Get user input for updating.
#   Create variables in the dict
#   Create all worlds
#   Then loop through all worlds and check each clause
#       We check if there's a world where both clauses are True, if the case they don't contradict and we do nothing


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
