

import random
import copy

import terminal
import function

class BaseSimulator(object):
    pass

def default_fitness(prog):
    s = prog.run()
    return s.registers[0]

default_config = {

    # Genetics/World options
    "population_size": 100,
    "max_generations": 200,
    "elite_rate": 0.1,
    "mutation_rate": 0.1,
    "simulator": BaseSimulator,
    "fitness_function": default_fitness,
    
    "max_program_length": 4,
    "min_program_length": 6,
    "num_registers": 4,
    "num_flags": 1,
    "constant_input_ratio": 0.5,

    # Data options
    "terminals": [terminal.TRegister, terminal.TConstant],
    "functions": [function.Add, function.Sub, function.Div, function.Mul, function.CompareGreater],
    "constants": [1, 2, 5, 10, 20, 50, 100],
    "constant_function": None,
    "output": True,
    "inputs": ["x", "y"]

}


def reduce_weights(inp):
    # TODO: This is bloated. Alternatives please...
    values = inp[:]
    
    # First, find the lowest weight (to optimize the output)
    lowest_weight = 1e1000
    for val in values:
        if isinstance(val, tuple) and val[1] < lowest_weight:
            lowest_weight = val[1]
        else:
            lowest_weight = 1
            break

    ret = []
    
    # divide out the weights so the smallest weight is 1.
    for i in xrange(len(values)):
        v = values[i]
        if isinstance(v, tuple):
            ret  += [v[0]] * (v[1] / lowest_weight)
        else:
            ret.append(v)

    return ret

        

class ProgramRunState(object):
    def __init__(self, program):
        
        self.program = program
        self.registers = [1] * program.config["num_registers"]
        self.flags     = [0] * program.config["num_flags"]
        self.simulator = program.config["simulator"]()
        self.inputs    = dict([(i, 0) for i in program.config["inputs"]])
        
        self.code_pointer = 0
        

class Program(object):
    def __init__(self, world):
        self.source = []
        self.world = world
        self.config = world.config
        
    def run(self, inputs = {}):
        state = ProgramRunState(self)
        
        if len(inputs) > 0:
            state.inputs = inputs
        
        codelen = len(self.source)
        while state.code_pointer < codelen and state.code_pointer >= 0:
            self.source[state.code_pointer].execute(state)
            state.code_pointer += 1

        return state

    def randomize(self):
        maxlen = self.config["max_program_length"]
        minlen = self.config["min_program_length"]
        stop_chance = 1.0 / float(maxlen - minlen + 1.0)

        # make sure we're between the max and min lengths, stopping
        # somewhere randomly inbetween.
        while len(self.source) < minlen or \
              (random.random() > stop_chance and len(self.source) < maxlen):

            newfunc = random.choice(self.world.functions)(self)
            self.source.append(newfunc)
            

    def copy_source(self):
        return copy.deepcopy(self.source)
    

class World(object):
    def __init__(self,  options = {}, **kwargs):
        self.config = default_config
        self.config.update(options)
        self.config.update(kwargs)

        # TODO: Make sure terminals don't appear in config['terminals'] if their
        # num is less than one. (num_flags, num_registers, num_inputs, etc)

        self.config["inputs"]    = reduce_weights(self.config["inputs"])
        self.config["constants"] = reduce_weights(self.config["constants"])
        
        self.functions = reduce_weights(self.config["functions"])
        self.terminals = reduce_weights(self.config["terminals"])
        
        # find out which terminals can be written to.
        self.terminals_writable = []
        for term in self.terminals:
            if term.readonly == False:
                self.terminals_writable.append(term)


    def new_program(self):
        p = Program(self)
        p.randomize()
        return p






        
