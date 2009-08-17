

import random
import copy


class BaseSimulator(object):
    pass


default_config = {

    # Genetics options
    "population_size": 100,
    "max_generations": 200,
    "elite_rate": 0.1,
    "mutation_rate": 0.1,
    "simulator": BaseSimulator,
    
    # Program options
    "max_program_length": 50,
    "min_program_length": 10,
    "num_registers": 4,
    "num_flags": 1,
    "num_inputs": 5,
    "constant_input_ratio": 0.5,

    # Data options
    "terminals": [],
    "functions": [],
    "constants": [1, 5, 10, 20, 50, 100],
    "inputs": [range(i, i+5) for i in xrange(5)]

}


def reduce_weights(inp):
    
    # TODO: This is bloated. Alternatives please...
    
    values = inp[:]
    # First, find the lowest weight (to optimize the output)
    lowest_weight = 1e1000
    for val in values:
        if isinstance(val, tuple):
            if val[1] < lowest_weight:
                lowest_weight = values[1]
        else:
            lowest_weight = 1
            break

    # divide out the weights so the smallest weight is 1.
    if lowest_weight > 1:
        values = map(lambda v: [v[0], v[1] / lowest_weight], values)

    ret = []
    
    for val in values:
        if isinstance(val, tuple):
            ret += [val[0]] * val[1]
        else:
            ret.append(val)

    return ret


        

class ProgramRunState(object):
    def __init__(self, program):
        self.program = program
        self.registers = [0] * program.config["num_registers"]
        self.flags     = [0] * program.config["num_flags"]
        self.simulator = program.config["simulator"]()
        

class Program(object):
    def __init__(self, world):
        self.source = []
        self.world = world
        # shortcut
        self.config = world.config
        
    def run(self):
        state = ProgramRunState(self)

        for func in self.source:
            func.execute(state)

        return state

    def randomize(self):
        maxlen = self.config["max_program_length"]
        minlen = self.config["min_program_length"]
        stop_chance = 1 / (maxlen - minlen)

        # make sure we're between the max and min lengths, stopping
        # somewhere randomly inbetween.
        while len(self.source) < minlen or \
              (random.random() > stop_chance and len(self.source) < maxlen):

            newfunc = random.choice(self.world.functions)
            

            

    def copy_source(self):
        return copy.deepcopy(self.source)
    

class World(object):
    def __init__(self,  options = [], **kwargs):
        self.config = default_config.update(options).update(kwargs)

        self.config["inputs"]    = reduce_weights(kwargs["inputs"])
        self.config["constants"] = reduce_weights(kwargs["constants"])
        
        self.functions = kwargs["functions"]
        self.terminals = kwargs["terminals"]
        
        # find out which terminals can be written to.
        self.terminals_writable = []
        for term in self.terminals:
            if term.readonly == False:
                self.terminals_writeable.append(term)










        
