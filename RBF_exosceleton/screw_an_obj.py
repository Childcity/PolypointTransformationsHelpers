import sys
import math
from obj_io import *

def screw_an_obj(INPUT, div):
    OUTPUT = INPUT.replace('.obj', f'_screwed_div_{div}.obj')

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
        angle = z / div
        d = (x**2 + y**2) ** 0.5
        new_x = math.sin(a + angle) * d
        new_y = math.cos(a + angle) * d
        new_z = z
        new_vs += [[new_x, new_y, new_z]]

    f = open(OUTPUT, 'w')
    f.write(str_from_vertexes(new_vs) + '\n' + str_from_faces(ts))
    f.close()

def generate_screwed():
    # in_model_path = './obj/tetr/tetr_13v_translated.obj'
    #in_model_path = './obj/tetr/sphere_transform/sphere_80t.obj'
    #in_model_path = './obj/sphere/sphere_80t.obj'
    #in_model_path = './obj/thorus/thorus_480v.obj'
    in_model_path = './obj/cube/cube_1.obj'
    screw_an_obj(in_model_path, 1)
    for div in range(600, 901, 50):
        screw_an_obj(in_model_path, div)
        print('screw with division', div)

if len(sys.argv) >= 3:
    screw_an_obj(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
else:
    print("Please specify the input obj file and the rotation divider (angle = z/DIV) in degrees")
    generate_screwed()
    exit(1)
