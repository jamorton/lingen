
import lingen

world = lingen.World()

p = world.new_program()

for i in p.source:
    print i.tostring()
