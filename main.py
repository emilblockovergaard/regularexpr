# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class Expr:
    is_true = False     # What the node evaluates to
    var_ref = None      # Reference to variable
    l_child = None      # Children
    r_child = None

    def __init__(self):
        is_true = False
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
        return not self.is_true


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # First we try to implement expression: "(A&B)|C" into our code simply being able to represent it
    # Then we might add how to input a expression
    # Then we can add revision and stuff

    # Variables/table
    var_a = True
    var_b = False
    var_c = False

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

    print("Eval2: "+ str(my_or.evaluate()))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
