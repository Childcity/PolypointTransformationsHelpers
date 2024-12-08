from RBF_exosceleton.obj_io import *
import numpy as np
import math
import time
import collections
from scipy.optimize import minimize

reg_term = 1e-16


class Plane:
	_nan_p = np.array([np.nan, np.nan, np.nan])

	id = -1

	A, B, C, D = np.nan, np.nan, np.nan, np.nan
	P1, P2, P3 = _nan_p, _nan_p, _nan_p

	@staticmethod
	def from_abcd(id, a, b, c, d):
		p = Plane()
		p.id = id
		p.A, p.B, p.C, p.D = a, b, c, d
		return p

	def __init__(self, id = -1, p1 = _nan_p, p2 = _nan_p, p3 = _nan_p):
		if np.any(np.isnan(p1)) or np.any(np.isnan(p2)) or np.any(np.isnan(p3)):
			return

		self.id = id
		self.P1, self.P2, self.P3 = p1, p2, p3

		# Calculate two vectors in the plane
		p2p1 = p2 - p1
		p3p1 = p3 - p1

		# Calculate the normal vector to the plane using the cross product
		normal_vector = np.cross(p2p1, p3p1)

		# Get plane coefficients
		self.A, self.B, self.C = normal_vector
		# if self.A == 0.0:
		# 	self.A = reg_term
		# if self.B == 0.0:
		# 	self.B = reg_term
		# if self.C == 0.0:
		# 	self.C = reg_term

		# Calculate the value of D for the plane equation ax + by + cz + d = 0
		self.D = -(self.A * p1[0] + self.B * p1[1] + self.C * p1[2])

	def __repr__(self):
		return f"Plane(id={id}; A={self.A}; B={self.B}; C={self.C}; D={self.D})"

	def __str__(self):
		return f"Plane(id={id}; A={self.A}; B={self.B}; C={self.C}; D={self.D})"

	def get_surface_for_z(self, X, Y): # X, Y: 2D arrays (2D grid)
		return (-self.A * X - self.B * Y - self.D) / self.C
 
	def length(self):
		# magnitude of the normal vector
		return math.sqrt(self.A ** 2 + self.B ** 2 + self.C ** 2)

	def normalized(self):
		magnitude = self.length()
		if magnitude == 0:
			return self
		else:
			return Plane.from_abcd(self.id, self.A / magnitude, self.B / magnitude, self.C / magnitude, self.D / magnitude)

	def sign_distance(self, point):
		A, B, C, D = self.A, self.B, self.C, self.D
		x, y, z = point
		return (A * x + B * y + C * z + D) / self.length()

	def distance(self, point):
		A, B, C, D = self.A, self.B, self.C, self.D
		x, y, z = point
		return (A * x + B * y + C * z + D) ** 2 / self.length()


Vertex = collections.namedtuple('Vertex', ['x', 'y', 'z'])


def build_planes(vertexes: list, triangles: list) -> (list[Plane], dict[Vertex, set[Plane]]):
	planes: list[Plane] = []
	planes_for_vertex_dict: dict[Vertex, set[Plane]] = {
		Vertex(*v_arr): set() for v_arr in vertexes # Initialize with empty sets, to preserve order of 'vertexes'
	}

	# NOTE: planes_for_vertex_dict stores each vertex as list of connected planes 

	def append_vertex_as_planes(point: list, plane: Plane):
		vertex_key = Vertex(*point)
		assert vertex_key in planes_for_vertex_dict
		planes_for_vertex_dict[vertex_key].add(plane)

	# Generate planes for each triangle
	for id, tri  in enumerate(triangles):
		p1 = np.array(triangle_point(vertexes, tri[0]))
		p2 = np.array(triangle_point(vertexes, tri[1]))
		p3 = np.array(triangle_point(vertexes, tri[2]))
		plane = Plane(id, p1, p2, p3)
		planes.append(plane)
		append_vertex_as_planes(p1, plane)
		append_vertex_as_planes(p2, plane)
		append_vertex_as_planes(p3, plane)
	return planes, planes_for_vertex_dict


def get_polypoint_plane(plane: Plane, orig_basises: list, res_basises: list):
	a1, b1, c1, d1, r1 = 0, 0, 0, 0, 0
	a2, b2, c2, d2, r2 = 0, 0, 0, 0, 0
	a3, b3, c3, d3, r3 = 0, 0, 0, 0, 0
	a4, b4, c4, d4, r4 = 0, 0, 0, 0, 0

	for orig_basis_p, res_basis_p in zip(orig_basises, res_basises):
		γ = plane.sign_distance(orig_basis_p)
		# print("orig_basis_p", orig_basis_p, "\t γ", γ)

		x = res_basis_p[0]
		y = res_basis_p[1]
		z = res_basis_p[2]
		# h = 1
		γSquered = γ ** 2

		a1 += x * x / γSquered
		b1 += x * y / γSquered
		c1 += x * z / γSquered
		d1 += x 	/ γSquered		# * h

		# a2 += y * x / γSquered	# a2 == b1
		b2 += y * y	/ γSquered
		c2 += y * z	/ γSquered
		d2 += y 	/ γSquered		# * h

		#a3 += z * x * γSquered		# a3 == c1
		#b3 += z * y * γSquered		# b3 == c2
		c3 += z * z	/ γSquered
		d3 += z 	/ γSquered		# * h

		#a4 += x / γSquered		# a4 == d1
		#b4 += y / γSquered		# b4 == d2
		#c4 += z / γSquered		# c4 == d3
		d4 += 1 / γSquered 		# * h * h
  
		r1 += x / γ
		r2 += y / γ
		r3 += z / γ
		r4 += 1 / γ

	# Add a small regularization term to the diagonal elements of A
	A = np.array([
		[a1 + reg_term, b1, c1, d1],
		[b1, b2 + reg_term, c2, d2],
		[c1, c2, c3 + reg_term, d3],
		[d1, d2, d3, d4 + reg_term]])

	B = np.array([r1, r2, r3, r4])
	X = np.linalg.solve(A, B)
	return Plane.from_abcd(plane.id, X[0], X[1], X[2], X[3])


def get_polypoint_planes_list(in_planes: list[Plane], orig_basises: list, res_basises: list) -> list[Plane]:
	start_time = time.time()
	result_planes: list = list()

	for plane in in_planes:
		tr_plane = get_polypoint_plane(plane, orig_basises, res_basises) # .normalized()
		assert tr_plane.id != -1
		result_planes.append(tr_plane)

	print(f"get_polypoint_planes_list(): {time.time() - start_time} seconds")
	return result_planes


def closest_point_to_planes_min(planes: list[Plane]) -> np.array:
	def objective_function(point: list, planes: list[Plane]):
		# The sum of squared distances to the planes
		return sum(plane.distance(point) for plane in planes)

	# Initial point (zero point) for the minimizer
	initial_point = (0, 0, 0)

	min_result = minimize(objective_function, initial_point, args=(planes,), method='L-BFGS-B')
	return min_result.x # closest_point


def closest_point_to_planes_lstsq(planes: list[Plane]):
	A = np.array([[plane.A, plane.B, plane.C] for plane in planes])
	B = np.array([-plane.D for plane in planes])
	X = np.linalg.lstsq(A, B, rcond=None)[0]
	return X


def closest_point_to_planes_pinv(planes: list[Plane]):
	A = np.array([[plane.A, plane.B, plane.C] for plane in planes])
	# A += np.eye(A.shape[0], A.shape[1]) * reg_term
	B = np.array([-plane.D for plane in planes])
	# Compute the pseudo-inverse of A
	A_pinv = np.linalg.pinv(A)
	# Get the least-squares solution to the A system
	return A_pinv.dot(B)


def get_transformed_vertexes(planes_for_vertex_dict: dict[Vertex, set[Plane]], tr_planes: list[Plane]) -> list[np.array]:
	# Get transformed vertexes by finding closest points to transformed planes
	result_vertexes : list[np.array] = []
	for planes_for_vertex_set in planes_for_vertex_dict.values():
		tr_planes_for_vertex_set: set[Plane] = set()

		# Find all transformed planes (by Plane.id) that will later represent transformed vertex
		for plane_for_vertex in planes_for_vertex_set:
			tr_planes_for_vertex_set.add(tr_planes[plane_for_vertex.id])

		# Find vertex after transformation
		result_vertexes.append(closest_point_to_planes_pinv(tr_planes_for_vertex_set))
	return result_vertexes


def export_pp_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO, DEFORMED_OUTPUT = None):
	if (DEFORMED_OUTPUT == None):
		DEFORMED_OUTPUT = DEFORMATION_BASIS_TO.split('/')[-1].replace('bunny_decimated', 'result_pp_deformed')

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

	print('low-polygonal models:\n\tdeformation basis from has', len(dbf_ts), 'triangles and \n\tdeformation basis to has', len(dbt_ts), 'triangles.\n')
	assert(len(dbf_ts) == len(dbt_ts))

	in_planes, in_planes_for_vertex_dict = build_planes(di_vs, di_ts)

	# Get transformed planes
	start_time = time.time()
	tr_planes = get_polypoint_planes_list(in_planes, orig_basises=dbf_vs, res_basises=dbt_vs)
	tr_vertexes  = get_transformed_vertexes(in_planes_for_vertex_dict, tr_planes)
	print(f"Transformation took: {time.time() - start_time} seconds")

	with open(DEFORMED_OUTPUT, 'w+') as f:
		print('exported pp deformed to', DEFORMED_OUTPUT)
		f.write(str_from_vertexes(tr_vertexes) + str_from_faces(di_ts))

def generate_pp_deformed():
    DEFORMATION_INPUT = './obj/bunny/bunny_1.obj'
    DEFORMATION_BASIS_FROM = './obj/bunny/bunny_decimated_1.obj'
    DEFORMATION_BASIS_TO_FIRST = './obj/bunny/bunny_decimated_1_screwed_div_1.obj'

    export_pp_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO_FIRST)
    for div in range(10, 61, 10):
        DEFORMATION_BASIS_TO = DEFORMATION_BASIS_TO_FIRST.replace('div_1', f'div_{div}')
        export_pp_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO)
        print('exported pp deformed with division', div, 'DEFORMATION_BASIS_TO:', DEFORMATION_BASIS_TO)

# def generate_pp_deformed():
#     DEFORMATION_INPUT_FIRST = './obj/bunny/bunny_1.obj'
#     DEFORMATION_BASIS_FROM = './obj/bunny/bunny_decimated_1.obj'
#     DEFORMATION_BASIS_TO = './obj/bunny/bunny_decimated_1_screwed_div_30.obj'

#     #export_pp_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO_FIRST)
#     for div in range(10, 10, 10):
#         DEFORMATION_INPUT = DEFORMATION_INPUT_FIRST.replace('bunny_1', f'bunny_decimated_{div}')
#         DEFORMED_OUTPUT = DEFORMATION_INPUT.split('/')[-1].replace('bunny', f'result_pp_deformed_1_screwed_div_30_bunny_decimated_{div}%')
#         export_pp_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO, DEFORMED_OUTPUT)
#         print('exported pp deformed with division', div, 'DEFORMATION_BASIS_TO:', DEFORMATION_BASIS_TO)


if __name__ == "__main__":
	# generate_pp_deformed()
 
    DEFORMATION_INPUT = './obj/bunny/bunny_1.obj'
    DEFORMATION_BASIS_FROM = './obj/tetr/tetr_4t.obj'
    DEFORMATION_BASIS_TO = './obj/tetr/tetr_deformed_4v_1_scaled_rotated_moved.obj'
    #DEFORMATION_BASIS_TO = './obj/tetr/tetr_deformed_13v_2.obj'
    DEFORMED_OUTPUT = DEFORMATION_BASIS_TO.replace('tetr_', 'test_result_pp_deformed_')

    export_pp_deformed(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO, DEFORMED_OUTPUT)

