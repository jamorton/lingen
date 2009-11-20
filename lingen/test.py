
import lingen
import terminal
import random


def ran():
    return random.randint(0, 10)

world = lingen.World(constant_function=ran, terminals=[terminal.TConstant, terminal.TRegister, terminal.TInput])
p = world.new_program()

s = p.run({"x": 12, "y": 5})

for i in p.source:
    print i.tostring()

print s.registers
print s.flags
