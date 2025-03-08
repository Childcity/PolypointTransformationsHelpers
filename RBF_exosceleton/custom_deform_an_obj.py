import sys
import math
from obj_io import *
import random

def custom_deform_an_obj(INPUT, div, rnd_d, defformed_output = None):
    if (defformed_output == None):
        defformed_output = INPUT.replace('.obj', f'_rnd1_{div}.obj')

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

    f = open(defformed_output, 'w')
    f.write(str_from_vertexes(new_vs) + '\n' + str_from_faces(ts))
    f.close()

#rnd_8_num = [[-0.08, -0.05, -0.01, -0.0, 0.05, 0.04, 0.09, -0.06], [-0.07, 0.05, 0.06, -0.07, 0.06, -0.05, -0.09, -0.08], [-0.04, -0.04, -0.1, -0.08, -0.07, -0.05, 0.06, -0.02], [-0.06, 0.02, -0.01, 0.04, 0.08, -0.07, 0.09, 0.1], [-0.03, -0.0, 0.03, -0.03, 0.08, 0.0, 0.1, 0.01], [0.09, 0.09, -0.02, 0.08, 0.04, 0.09, -0.09, -0.06], [0.01, 0.06, -0.1, -0.01, -0.05, -0.01, 0.08, -0.03], [0.01, 0.09, 0.04, 0.04, -0.02, -0.05, -0.03, -0.07], [-0.02, 0.06, 0.01, 0.01, -0.07, 0.02, 0.05, -0.01], [-0.05, -0.03, -0.08, -0.04, -0.05, 0.08, -0.06, -0.09], [0.02, -0.01, 0.02, 0.09, -0.07, 0.05, -0.07, 0.09], [0.1, 0.01, -0.08, 0.07, -0.04, 0.1, -0.06, -0.1]]

def generate_deformed():
    in_model_path = './obj/cube_2/cube_2.obj'
    in_model_path = './obj/cube_2/torus_156v.obj'
    for div in range(1, 11, 1):
        #div = div / 10
        custom_deform_an_obj(in_model_path, div, rnd_8_num[div])
        print('screw with division', div)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        custom_deform_an_obj(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
    else:
        print("Please specify the input obj file and the rotation divider (angle = z/DIV) in degrees")
        generate_deformed()
        exit(1)

# staticaly initialize a 2d array with 12 elements
# each element is random number from -0.5 to 0.5
# round to 2 decimal places
# d = [[round(random.uniform(-0.5, 0.5), 2) for i in range(4)] for j in range(12)]
# print(d)
