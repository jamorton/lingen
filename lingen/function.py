
from random import  choice
    

class Function(object):
    has_output = False
    num_args   = 0
    function_str  = None
    def __init__(self, program):
        self.program = program

        if self.has_output == True:
            if len(program.world.terminals_writable) < 1:
                raise Exception("No writable terminals for function output!")
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
        if self.function_str == None:
            self.function_str = self.__class__.__name__.lower()
        # Bleh...
        ostr = ", ".join([i.tostring() for i in self.inputs])
        ostr = self.function_str + " (" + ostr + ")"
        if self.has_output:
            ostr = self.output.tostring() + " = " + ostr

        return ostr


class ArithmeticFunction(Function):
    has_output = True
    num_args = 2
    function_str = "<arithmetic>"
    
    def tostring(self):
        return ' '.join((self.output.tostring(), "=", self.inputs[0].tostring(),
                         self.function_str, self.inputs[1].tostring()))


    
class FAdd(ArithmeticFunction):
    function_str = "+"
    
    def run(self, state):
        return self.input(0) + self.input(1)

class FSub(ArithmeticFunction):
    function_str = "-"
    
    def run(self, state):
        return self.input(0) - self.input(1)

class FDiv(ArithmeticFunction):
    function_str = "/"

    def run(self, state):
        return self.input(0) / self.input(1)

class FMul(ArithmeticFunction):
    function_str = "*"

    def run(self, state):
        return self.ipnut(0) * self.input(1)


