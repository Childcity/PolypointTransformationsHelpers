import sys
import math
from obj_io import *

def spiral_screw_an_obj(INPUT, div, max_radius):
    OUTPUT = INPUT.replace('.obj', f'_radial_scale_div_{div}.obj')

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
        scale = 1 + z / div
        new_x = x * scale
        new_y = y * scale
        new_z = z
        new_vs += [[new_x, new_y, new_z]]

    f = open(OUTPUT, 'w')
    f.write(str_from_vertexes(new_vs) + '\n' + str_from_faces(ts))
    f.close()

def generate_screwed():
    in_model_path = './obj/cube/test/cube_1.obj'
    in_model_path = './obj/thorus/test/thorus_480v.obj'
    #screw_an_obj(in_model_path, 1)
    for div in range(100, 401, 20):
        spiral_screw_an_obj(in_model_path, div, 70)
        print('screw with division', div)

if len(sys.argv) >= 3:
    spiral_screw_an_obj(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
else:
    print("Please specify the input obj file and the rotation divider (angle = z/DIV) in degrees")
    generate_screwed()
    exit(1)
