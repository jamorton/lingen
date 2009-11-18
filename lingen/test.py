
import lingen
import terminal
import random


def ran():
    return random.randint(0, 10)

world = lingen.World(constant_function=ran, terminals=[terminal.TConstant, terminal.TRegister])
p = world.new_program()

s = p.run()

#for i in p.source:
#    print i.tostring()

print s.registers
