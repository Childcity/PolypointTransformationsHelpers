import sys
import math
from obj_io import *

if len(sys.argv) < 4:
    print("Please specify the input obj file, wave amplitude and period")
    exit(1)

INPUT = sys.argv[1]
amplitude = float(sys.argv[2])
period = float(sys.argv[3])

OUTPUT = INPUT.replace('.', '_waved_a_' + sys.argv[2] + '_t_' + sys.argv[3] + '.')

f = open(INPUT, 'r')
di = f.read()
f.close()
vs = vertexes(di)
ts = triangles(di)

new_vs = []
for v in vs:
    x = v[0]
    y = v[1]
    z = v[2]
    skew = amplitude * math.sin(z/period)
    new_x = x + skew
    new_y = y
    new_z = z
    new_vs += [[new_x, new_y, new_z]]

f = open(OUTPUT, 'w')
f.write(str_from_vertexes(new_vs) + str_from_faces(ts))
f.close()
