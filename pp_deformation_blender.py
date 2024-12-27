import subprocess
import sys
import os

# Workaround for Blender's Python environment. Add the path of pp_deformation to sys.path
sys.path.insert(1, 'D:\Projects\Python\PolypointTransformationsHelpers')
from pp_deformation import *

try:
	import numpy as np
	from scipy.optimize import minimize
except ImportError:
	# Install modules for Blender's Python env
	python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
	subprocess.call([python_exe, "-m", "ensurepip"])
	subprocess.call([python_exe, "-m", "pip", "install", "--target", "C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\lib\site-packages", 
                    "scipy", "numpy"])

import numpy as np
from scipy.optimize import minimize
import math
import bpy
from bpy.types import BlendDataObjects, Object
from copy import deepcopy

# Helper functions
# def get_mesh_data(obj: Object):
#	 """Get vertices and faces from a Blender object."""
#	 mesh = obj.data
#	 vertices = np.array([v.co for v in mesh.vertices])
#	 faces = [tuple(p.vertices) for p in mesh.polygons]
#	 return vertices, faces

# def set_mesh_data(obj: Object, vertices):
#	 """Set vertices in a Blender object."""
#	 mesh = obj.data
#	 for i, coord in enumerate(vertices):
#		 mesh.vertices[i].co = coord
	
def get_mesh_data(obj: Object):
	"""Get vertices and faces from a Blender object."""
	mesh = obj.data
	vertices = [[v.co.x, v.co.y, v.co.z] for v in mesh.vertices]
	faces = [[p.vertices[0], p.vertices[1], p.vertices[2], ] for p in mesh.polygons]
	return vertices, faces

def set_mesh_data(obj: Object, vertices: list):
	"""Set vertices in a Blender object."""
 
	if obj.mode == 'EDIT':
		bpy.ops.object.mode_set(mode='OBJECT')
  
	mesh = obj.data
	for i, coord in enumerate(vertices):
		mesh.vertices[i].co = coord
  
	mesh.update()
	mesh.validate()
 
	bpy.ops.object.mode_set(mode='EDIT')

# Main function
def deform_mesh(input_name, deformation_basis_from_name, deformation_basis_to_name, output_name):
	input_obj = bpy.data.objects[input_name]
	basis_from_obj = bpy.data.objects[deformation_basis_from_name]
	basis_to_obj = bpy.data.objects[deformation_basis_to_name]
	output_obj = bpy.data.objects[output_name]

	# Get mesh data
	input_vertices, input_faces = get_mesh_data(input_obj)
	basis_from_vertices, basis_from_faces = get_mesh_data(basis_from_obj)
	basis_to_vertices, basis_to_faces = get_mesh_data(basis_to_obj)
	# print("Input Vertices:", input_vertices)
	# print("Input Triangles:", input_faces)

	# Build planes from faces
	in_planes, in_planes_for_vertex_dict = build_planes(input_vertices, input_faces)

	# Get transformed planes
	start_time = time.time()
	tr_planes = get_polypoint_planes_list(in_planes, orig_basises=basis_from_vertices, res_basises=basis_to_vertices)
	tr_vertexes  = get_transformed_vertexes(in_planes_for_vertex_dict, tr_planes)
	print(f"Transformation took: {time.time() - start_time} seconds")

	# Apply deformation to output object
	set_mesh_data(output_obj, tr_vertexes)

# Parameters
DEFORMATION_INPUT = "icosphere"
DEFORMATION_BASIS_FROM = "tetr_13v"
DEFORMATION_BASIS_TO = "tetr_deformed_13v_4"
DEFORMED_OUTPUT = "result_pp_deformed_13v_4"

#deform_mesh(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO, DEFORMED_OUTPUT)

last_basis_to_vertices = None

def update_deformation(scene):
	global last_basis_to_vertices
 
	basis_to_obj = bpy.data.objects[DEFORMATION_BASIS_TO]
	basis_to_vertices, basis_to_faces = get_mesh_data(basis_to_obj)
	if basis_to_vertices == last_basis_to_vertices:
		return
	last_basis_to_vertices = deepcopy(basis_to_vertices)	
 
	print(f"{DEFORMATION_BASIS_TO} updated, recalculating deformation...")
	deform_mesh(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO, DEFORMED_OUTPUT)

# Register the handler
bpy.app.handlers.depsgraph_update_post.append(update_deformation)