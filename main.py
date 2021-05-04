# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Sikre at expr virker korrekt
# Input, tjek det er korrekt

# Plausability table

# Consistency check

class Expr:
    var_ref = None      # Reference to variable

    l_child = None      # Children
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

        print("Error node is full! Can't add child!")
        return False

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

    #print("Eval2: "+ str(my_or.evaluate()))

    str_in = input("Input a belief in CN-Form: ")
    # Find pairs of "(" and ")"
    # Test string: ((A&B)&(C|B))&(A|B)      CNF form ->     A & B & (C|B) & (A|B)
    # (A&B)&C -> A&B&C

    pair_list = []

    str_in = str_in.replace(" ","")
    print(str_in)

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

    # things = []

    subs = str_in.split("&")

    for x in subs:
        print(x)

    head = AndExpr()
    for i in range(0, len(subs)):
        print(head.add_child(subs[i]))



    #print("Left par: %d \t Right par: %d" % (first_right, first_left))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
