import sys
import math
from obj_io import *

if len(sys.argv) < 3:
    print("Please specify the input obj file and the rotation angle in degrees")
    exit(1)

INPUT = sys.argv[1]
angle = int(sys.argv[2]) / 180. * math.pi

OUTPUT = INPUT.replace('.', '_rotated_z_' + sys.argv[2] + '.')

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
    a = math.atan2(x, y)
    d = (x**2 + y**2) ** 0.5
    new_x = math.sin(a + angle) * d
    new_y = math.cos(a + angle) * d
    new_z = z 
    new_vs += [[new_x, new_y, new_z]]

f = open(OUTPUT, 'w')
f.write(str_from_vertexes(new_vs) + str_from_faces(ts))
f.close()
