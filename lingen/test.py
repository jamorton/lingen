
import lingen
import terminal
import random


def ran():
    return random.randint(0, 10)


settings = {
     'terminals': [terminal.Constant, terminal.Register, terminal.Input]
}

world = lingen.World(settings, constant_function=ran)
p = world.new_program()

s = p.run({"x": 12, "y": 5})

for i in p.source:
    print i.tostring()

print s.registers
print s.flags
