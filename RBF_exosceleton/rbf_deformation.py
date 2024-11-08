from obj_io import *
import numpy as np

DEFORMATION_INPUT = 'bunny.obj'
MODEL_TO_COMPARE_WITH = 'bunny_rotated_z_10.obj'
DEFORMATION_BASIS_FROM = 'bunny_decimated.obj'
DEFORMATION_BASIS_TO = 'bunny_decimated_rotated_z_10.obj'

f = open(DEFORMATION_INPUT, 'r')
di = f.read()
f.close()
di_vs = vertexes(di)
di_ts = triangles(di)

f = open(MODEL_TO_COMPARE_WITH, 'r')
mtcw = f.read()
f.close()
mtcw_vs = vertexes(mtcw)
mtcw_ts = triangles(mtcw)

f = open(DEFORMATION_BASIS_FROM, 'r')
dbf = f.read()
f.close()
dbf_vs = vertexes(dbf)
dbf_ts = triangles(dbf)

f = open(DEFORMATION_BASIS_TO, 'r')
dbt = f.read()
f.close()
dbt_vs = vertexes(dbt)
dbt_ts = triangles(dbt)

print('low-polygonal models:\n\tdeformation basis from has', len(dbf_ts), 'triangles and \n\tdeformation basis to has', len(dbt_ts), 'triangles.\n')
print('high-polygonal models:\n\tdeformation input has', len(di_ts), 'triangles and \n\tmodel to compare with has', len(mtcw_ts), 'triangles.')


# radial basis functions
def radial(x, xi):
    # this is the simplest possible radial function. We'll try several different ones
    delta = np.array(x) - np.array(xi)
    distance = np.dot(delta, delta)**0.5
    return distance

def Ys_for_points(ps, rns):
    A = []
    B = []
    for i in range(len(ps)):
        Ai = []
        for j in range(len(ps)):
            Ai += [radial(ps[i], ps[j])]
        A += [Ai]
        B += [[rns[i]]]

    Ys = np.linalg.solve(A, B)
    # warning! Ys is not a list but a 1xN matrix
    return Ys

def RBF(xyz, Ys, ps):
    sum = 0.
    for i in range(len(ps)):
        sum += Ys[i][0] * radial(xyz, ps[i])
    return sum

dxs = []
dys = []
dzs = []

assert(len(dbf_vs) == len(dbt_vs))
for i in range(len(dbf_vs)):
    dxs += [dbt_vs[i][0] - dbf_vs[i][0]]
    dys += [dbt_vs[i][1] - dbf_vs[i][1]]
    dzs += [dbt_vs[i][2] - dbf_vs[i][2]]

Yxs = Ys_for_points(dbf_vs, dxs)
Yys = Ys_for_points(dbf_vs, dys)
Yzs = Ys_for_points(dbf_vs, dzs)

deformed_vertices = []
for v in di_vs:
    new_x = v[0] + RBF(v, Yxs, dbf_vs)
    new_y = v[1] + RBF(v, Yys, dbf_vs)
    new_z = v[2] + RBF(v, Yzs, dbf_vs)
    deformed_vertices += [[new_x, new_y, new_z]]

f = open('__rbf_deformed.obj', 'w')
f.write(str_from_vertexes(deformed_vertices) + str_from_faces(di_ts))
f.close()
