
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
        raise Exception("write not implemented! (maybe set readonly to True?)")
    
    def tostring(self):
        return "<" + self.__class__.__name+ ">"

class TRegister(Terminal):
    readonly = False
    
    def randomize(self, program):
        # register number
        self.register = randint(0, program.config["num_registers"] - 1)

    def evaluate(self, state):
        return state.registers[self.register]

    def write(self, state, value):
        state.registers[self.registers] = value

    def tostring(self):
        return "register[" + self.register + "]"

class TConstant(Terminal):
    readonly = True
    value = 0
    def randomize(self, program):
        self.value = choice(program.config["constants"])

    def evaluate(self, state):
        return self.value

    def tostring(self):
        return str(self.value)

