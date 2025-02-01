import sys
import math
from obj_io import *

def spiral_screw_an_obj(INPUT, div, max_radius):
    OUTPUT = INPUT.replace('.obj', f'_mul_{div}.obj')

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
        scale = x*y*z
        new_x = x + div*scale
        new_y =  y + div*scale
        new_z = z + div*scale
        new_vs += [[new_x, new_y, new_z]]

    f = open(OUTPUT, 'w')
    f.write(str_from_vertexes(new_vs) + '\n' + str_from_faces(ts))
    f.close()

def generate_screwed():
    in_model_path = './obj/cube_2/cube_2.obj'
    in_model_path = './obj/cube_2/torus_156v.obj'
    for div in range(1, 11, 1):
        div = div / 10
        spiral_screw_an_obj(in_model_path, div, 70)
        print('screw with division', div)

if len(sys.argv) >= 3:
    spiral_screw_an_obj(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
else:
    print("Please specify the input obj file and the rotation divider (angle = z/DIV) in degrees")
    generate_screwed()
    exit(1)
