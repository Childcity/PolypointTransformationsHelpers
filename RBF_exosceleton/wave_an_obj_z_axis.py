import sys
import math
from obj_io import *

def wave_an_obj_z_axis(INPUT, amplitude, period):
    OUTPUT = INPUT.replace('.obj', f'_waved_a_{amplitude}_p_{period}.obj')

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

def generate_waved():
    in_model_path = './obj/tetr/tetr_13v.obj'
    period = 10
    wave_an_obj_z_axis(in_model_path, 1, period)
    for amplitude in range(10, 61, 10):
        wave_an_obj_z_axis(in_model_path, amplitude, period)
        print('waved with amplitude', amplitude, 'and period', period)

if len(sys.argv) >= 4:
    wave_an_obj_z_axis(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
else:
    print("Please specify the input obj file, wave amplitude and period")
    generate_waved()
    exit(1)
