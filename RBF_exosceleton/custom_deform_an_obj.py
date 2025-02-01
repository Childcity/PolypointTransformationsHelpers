import sys
import math
from obj_io import *
import random

def spiral_screw_an_obj(INPUT, div, rnd_d):
    OUTPUT = INPUT.replace('.obj', f'_rnd1_{div}.obj')

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

        d1, d2, d3, d4, d5, d6, d7, d8 = rnd_d[0], rnd_d[1], rnd_d[2], rnd_d[3], rnd_d[4], rnd_d[5], rnd_d[6], rnd_d[7]
        s1 = (1-x)*y*z 
        s2 = x*(1-y)*z
        s3 = x*y*(1-z)
        s4 = (1-x)*(1-y)*z
        s5 = x*(1-y)*(1-z)
        s6 = (1-x)*y*(1-z)
        s7 = x*y*z
        s8 = (1-x)*(1-y)*(1-z)
        new_x = x + d1*s1 + d2*s2 + d3*s3 + d4*s4 + d5*s5 + d6*s6 + d7*s7 + d8*s8
        new_y = y + d1*s1 + d2*s2 + d3*s3 + d4*s4 + d5*s5 + d6*s6 + d7*s7 + d8*s8
        new_z = z + d1*s1 + d2*s2 + d3*s3 + d4*s4 + d5*s5 + d6*s6 + d7*s7 + d8*s8

        new_vs += [[new_x, new_y, new_z]]

    f = open(OUTPUT, 'w')
    f.write(str_from_vertexes(new_vs) + '\n' + str_from_faces(ts))
    f.close()

rnd_4_num = [[0.42, -0.33, 0.24, 0.25], [0.18, -0.15, 0.5, -0.12], [0.47, 0.28, 0.15, 0.36], [-0.17, 0.3, -0.28, 0.49], [-0.39, 0.21, 0.42, 0.15], [0.45, -0.38, 0.3, 0.08], [0.42, -0.1, -0.47, 0.3], [0.49, 0.44, 0.46, -0.1], [0.01, -0.38, 0.18, -0.28], [-0.31, 0.31, 0.24, 0.06], [0.22, -0.41, -0.42, 0.28], [0.28, -0.42, -0.47, -0.49]]
rnd_4_num = [
    [0.42, -0.33, 0.24, 0.25], 
    [0.18, -0.15, 0.5, -0.12], 
    [0.47, 0.28, 0.15, 0.36], 
    [-0.17, 0.3, -0.28, 0.49], 
    [-0.39, 0.21, 0.42, 0.15], 
    [0.45, -0.38, 0.3, 0.08], 
    [0.42, -0.1, -0.47, 0.3], 
    [0.49, 0.44, 0.46, -0.1], 
    [0.01, -0.38, 0.18, -0.28], 
    [-0.31, 0.31, 0.24, 0.06], 
    [0.22, -0.41, -0.42, 0.28], 
    [0.28, -0.42, -0.47, -0.49]
]

def generate_screwed():
    in_model_path = './obj/cube_2/cube_2.obj'
    #in_model_path = './obj/cube_2/torus_156v.obj'
    for div in range(1, 11, 1):
        div = div / 10
        spiral_screw_an_obj(in_model_path, div, rnd_4_num[div])
        print('screw with division', div)

if len(sys.argv) >= 3:
    spiral_screw_an_obj(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
else:
    d = [[round(random.uniform(-0.1, 0.1), 2) for i in range(8)] for j in range(12)]
    print(d)
    print("Please specify the input obj file and the rotation divider (angle = z/DIV) in degrees")
    #generate_screwed()
    exit(1)

# staticaly initialize a 2d array with 12 elements
# each element is random number from -0.5 to 0.5
# round to 2 decimal places
# d = [[round(random.uniform(-0.5, 0.5), 2) for i in range(4)] for j in range(12)]
# print(d)
