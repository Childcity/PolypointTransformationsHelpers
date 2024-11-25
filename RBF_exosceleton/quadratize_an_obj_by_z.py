import sys
import math
from obj_io import *

def quadratize_an_obj_by_z(INPUT, div):
    OUTPUT = INPUT.replace('.obj', f'_squared_by_z_div_{div}.obj')

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
        new_x = x
        new_y = y
        new_z = (z/div)**2*div
        new_vs += [[new_x, new_y, new_z]]

    f = open(OUTPUT, 'w')
    f.write(str_from_vertexes(new_vs) + str_from_faces(ts))
    f.close()

def generate_quadratized():
    in_model_path = './obj/bunny/bunny_decimated_1.obj'
    quadratize_an_obj_by_z(in_model_path, 1)
    for div in range(10, 61, 10):
        quadratize_an_obj_by_z(in_model_path, div)
        print('squared with division', div)

if len(sys.argv) >= 3:
    quadratize_an_obj_by_z(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
else:
    print("Please specify the input obj file, and the z divider new_z = (z/div)^2*div")
    generate_quadratized()
    exit(1)
