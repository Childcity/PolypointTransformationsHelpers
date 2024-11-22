import sys
import math
from obj_io import *

if len(sys.argv) < 5:
    print("Please specify the input obj file and translation d_x, d_y, d_z")
    exit(1)

INPUT = sys.argv[1]
d_x, d_y, d_z = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])

OUTPUT = INPUT.replace('.', f'_translated_x_{d_x}_y_{d_y}_z_{d_z}.')

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
    new_x = x + d_x
    new_y = y + d_y
    new_z = z + d_z
    new_vs += [[new_x, new_y, new_z]]

f = open(OUTPUT, 'w')
f.write(str_from_vertexes(new_vs) + str_from_faces(ts))
f.close()
