
from random import randint, choice
    
class Function(object):
    has_output = False
    num_args   = 0
    def __init__(self, program):
        self.program = program

        if self.has_output == True:
            self.output = choice(program.world.terminals_writable)

        terms = program.world.terminals
        self.inputs = [choice(terms) for i in xrange(self.num_args)]

        self.curstate = None
        
    def execute(self, state):
        self.curstate = state
        
        if self.has_output:
            self.output.write(state, self.run(state))
        else:
            self.run(state)

        self.curstate = None

    def run(self, state):
        raise Exception("run not implemented!")

    def input(self,  t):
        """ shortcut to evalute an input terminal """
        return self.inputs[t].evaluate(self.curstate)

    def tostring(self):
        if self.has_output:
            return self.output.tostring() + \
                " = <" + self.__class__.__name__ + ">(" + \
                ' '.join(self.inputs) + ")"

class ArithmeticFunction(Function):
    has_output = True
    num_args = 2
    arithmetic_str = "<arithmetic>"

    def tostring(self):
        return ' '.join((self.output.tostring(),  "=", self.inputs[0].tostring(),
             self.arithmetic_str, self.inputs[1].tostring()))


class FAdd(ArithmeticFunction):
    arithmetic_str = "+"
    
    def run(self, state):
        return self.input(0) + self.input(1)

class FSubtract(ArithmeticFunction):
    arithmetic_str = "-"
    
    def run(self, state):
        return self.input(0) - self.input(1)

class FDivide(ArithmeticFunction):
    arithmetic_str = "/"

    def run(self, state):
        return self.input(0) / self.input(1)

class FMultiply(ArithmeticFunction):
    arithmetic_str = "*"

    def run(self, state):
        return self.ipnut(0) * self.input(1)


