from obj_io import *
import numpy as np
import time

# DEFORMATION_INPUT = 'bunny.obj'
# MODEL_TO_COMPARE_WITH = 'bunny_rotated_z_10.obj'
# DEFORMATION_BASIS_FROM = 'bunny_decimated.obj'
# DEFORMATION_BASIS_TO = 'bunny_decimated_rotated_z_10.obj'

# DEFORMATION_INPUT = './obj/bunny/bunny_1.obj'
# MODEL_TO_COMPARE_WITH = './obj/bunny/bunny_1.obj'
# DEFORMATION_BASIS_FROM = './obj/bunny/bunny_decimated_1.obj'
# DEFORMATION_BASIS_TO = './obj/bunny/bunny_decimated_1_screwed_div_50.obj'
# DEFORMATION_BASIS_TO = './obj/bunny/bunny_decimated_1_screwed_div_30.obj'
# DEFORMATION_BASIS_TO = './obj/bunny/bunny_decimated_1_waved_a_10_t_10.obj'

# DEFORMATION_INPUT = './obj/bunny/bunny.obj'
# DEFORMATION_BASIS_FROM = './obj/bunny/bunny_decimated_0.obj'
# DEFORMATION_BASIS_TO = './obj/bunny/bunny_decimated_0_screwed_div_50.obj'
# DEFORMATION_BASIS_TO = './obj/bunny/bunny_decimated_0_waved_a_10_t_10.obj'

def export_rbf_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO):
    f = open(DEFORMATION_INPUT, 'r')
    di = f.read()
    f.close()
    di_vs = vertexes(di)
    di_ts = triangles(di)

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

    start_time = time.time()

    deformed_vertices = []
    for v in di_vs:
        new_x = v[0] + RBF(v, Yxs, dbf_vs)
        new_y = v[1] + RBF(v, Yys, dbf_vs)
        new_z = v[2] + RBF(v, Yzs, dbf_vs)
        deformed_vertices += [[new_x, new_y, new_z]]

    print(f"Transformation took: {time.time() - start_time} seconds")

    f = open(DEFORMATION_BASIS_TO.split('/')[-1].replace('bunny_decimated', 'result_rbf_deformed'), 'w+')
    f.write(str_from_vertexes(deformed_vertices) + str_from_faces(di_ts))
    f.close()

def generate_rbf_deformed():
    DEFORMATION_INPUT = './obj/bunny/bunny_1.obj'
    DEFORMATION_BASIS_FROM = './obj/bunny/bunny_decimated_1.obj'
    DEFORMATION_BASIS_TO_FIRST = './obj/bunny/bunny_decimated_1_squared_by_z_div_1.obj'

    export_rbf_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO_FIRST)
    for div in range(10, 61, 10):
        DEFORMATION_BASIS_TO = DEFORMATION_BASIS_TO_FIRST.replace('div_1', f'div_{div}')
        export_rbf_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO)
        print('exported rbf deformed with division', div, 'DEFORMATION_BASIS_TO:', DEFORMATION_BASIS_TO)

if __name__ == "__main__":
    generate_rbf_deformed()