
from random import randint, choice

class Terminal(object):
    readonly = True
    
    def __init__(self, program):
        self.randomize(program)

    def randomize(self, program):
        raise Exception("randomize not implemented!")
    
    def evaluate(self, state):
        raise Exception("evaluate not implemented!")

    def write(self, state, value):
        raise Exception("write not implemented! (set terminal readonly to False?)")
    
    def tostring(self):
        return "<" + self.__class__.__name+ ">"

    
class Register(Terminal):
    readonly = False
    
    def randomize(self, program):
        # register number
        self.register = randint(0, program.config["num_registers"] - 1)

    def evaluate(self, state):
        return state.registers[self.register]

    def write(self, state, value):
        state.registers[self.register] = value

    def tostring(self):
        return "r" + str(self.register)

    
class Constant(Terminal):
    readonly = True
    value = 0
    
    def randomize(self, program):
        if program.config["constant_function"] is not None:
            self.value = program.config["constant_function"]()
        else:
            self.value = choice(program.config["constants"])

    def evaluate(self, state):
        return self.value

    def tostring(self):
        return str(self.value)


class Input(Terminal):
    readonly = True
    key = None
    
    def randomize(self, program):
        self.key = choice(program.config["inputs"])
        
    def evaluate(self, state):
        return state.inputs[self.key]

    def tostring(self):
        return self.key
