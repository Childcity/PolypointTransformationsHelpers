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
import traceback

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
def deform_mesh(input_name, deformation_basis_from_name, deformation_basis_to_name, output_name, topology):
	input_obj = bpy.data.objects[input_name]
	basis_from_obj = bpy.data.objects[deformation_basis_from_name]
	basis_to_obj = bpy.data.objects[deformation_basis_to_name]
	output_obj = bpy.data.objects[output_name]

	# Get mesh data
	input_vertices, input_faces = get_mesh_data(input_obj)
	print("Input Vertices:", input_vertices[0])
	basis_from_vertices, basis_from_faces = get_mesh_data(basis_from_obj)
	basis_to_vertices, basis_to_faces = get_mesh_data(basis_to_obj)
	# print("Input Vertices:", input_vertices)
	# print("Input Triangles:", input_faces)

	# Build planes from faces
	in_planes, in_planes_for_vertex_dict = build_planes(input_vertices, input_faces, topology)

	# Get transformed planes
	start_time = time.time()
	tr_planes = get_polypoint_planes_list(in_planes, orig_basises=basis_from_vertices, res_basises=basis_to_vertices)
	tr_vertexes  = get_transformed_vertexes(in_planes_for_vertex_dict, tr_planes, topology)
	print(f"Transformation took: {time.time() - start_time} seconds")

	# Apply deformation to output object
	set_mesh_data(output_obj, tr_vertexes)

# Parameters
DEFORMATION_INPUT = "thorus_80v"
# DEFORMATION_BASIS_FROM = "cube_1"
# DEFORMATION_BASIS_TO = "cube_1_screwed_div_901"
DEFORMATION_BASIS_FROM = "icosphere_80v"
DEFORMATION_BASIS_TO = "icosphere_deformed_80v"
DEFORMED_OUTPUT = "pp_thorus_deformed_80v"
topology = Topology.Intersect

#deform_mesh(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO, DEFORMED_OUTPUT)

def compare_listcomp(x, y):
    if x is None or y is None:
        return x is None and y is None  # Both must be None to return True
    if len(x) != len(y):  # Check length first
        return False
    for i, j in zip(x, y):
        if i != j:
            return False
    return True

last_basis_to_vertices = None

def update_deformation(scene):
	global last_basis_to_vertices
 
	basis_to_obj = bpy.data.objects[DEFORMATION_BASIS_TO]
	basis_to_vertices, basis_to_faces = get_mesh_data(basis_to_obj)
	if compare_listcomp(basis_to_vertices, last_basis_to_vertices):
		print("No changes in", DEFORMATION_BASIS_TO, ", skipping update")
		return
	last_basis_to_vertices = deepcopy(basis_to_vertices)	
 
	try:
		deform_mesh(DEFORMATION_INPUT, DEFORMATION_BASIS_FROM, DEFORMATION_BASIS_TO, DEFORMED_OUTPUT, topology)
		print(f"{DEFORMATION_BASIS_TO} updated, recalculating deformation...")
	except Exception as e:
		print(f"============================ Failed (topo={topology}): {traceback.format_exc()}")

# Register the handler
bpy.app.handlers.depsgraph_update_post.clear()
bpy.app.handlers.depsgraph_update_post.append(update_deformation)

# NOTE: to auto apply, select Edit -> change vertexes -> Unselect -> Save -> Select any vertex.
# NOTE: we can't mix .obj deformed models and models created in Blender because of different AXIS during export/import.
# NOTE: export IN/OUT model and IN/OUT basises to .obj and then import them back to Blender to have comparable AXIS.