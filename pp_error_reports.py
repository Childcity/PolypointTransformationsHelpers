import os
from openpyxl import Workbook
import numpy as np
from RBF_exosceleton.obj_io import *

def list_files(directory, startswith, extension):
	"""List files in a directory that start with a given string and have a given extension."""
	return [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if f.startswith(startswith) and f.endswith('.' + extension)]

def mean_squared_error(vertices1, vertices2):
	"""Compute the mean squared error between two sets of vertices."""
	vertices1 = np.array(vertices1)
	vertices2 = np.array(vertices2)
	return np.square(np.subtract(vertices1, vertices2)).mean()

def generate_deformed_report(subdir, pp_sidor_deformed_basename, pp_deformed_basename, pp_ort_deformed_basename, rbf_deformed_basename, excel_filename):

	all_pp_sidor_deformed = list_files(subdir, pp_sidor_deformed_basename, 'obj')
	all_pp_deformed = list_files(subdir, pp_deformed_basename, 'obj')
	all_pp_ort_deformed = list_files(subdir, pp_ort_deformed_basename, 'obj')
	all_rbf_deformed = list_files(subdir, rbf_deformed_basename, 'obj')

	assert len(all_pp_sidor_deformed) == len(all_pp_deformed) == len(all_pp_ort_deformed) == len(all_rbf_deformed), "Mismatch in file counts!"

	# Create Excel workbook
	workbook = Workbook()
	sheet = workbook.active
	sheet.title = f"{(excel_filename.split('.')[0]).replace('_', ' ')}"

	# Write header
	sheet.append(['Params', 'MSE (Sidor-RBF) ', 'MSE (Intersect-RBF)', 'MSE (Orthogonal-RBF)'])

	for file_index, (pp_sidor_file, pp_file, pp_ort_file, rbf_file) in enumerate(zip(all_pp_sidor_deformed, all_pp_deformed, all_pp_ort_deformed, all_rbf_deformed)):
		with open(pp_sidor_file, 'r') as f:
			pp_sidor_deformed_vertexes = vertexes(f.read())
		with open(pp_file, 'r') as f:
			pp_deformed_vertexes = vertexes(f.read())
		with open(pp_ort_file, 'r') as f:
			pp_ort_deformed_vertexes = vertexes(f.read())
		with open(rbf_file, 'r') as f:
			rbf_deformed_vertexes = vertexes(f.read())

		assert len(pp_sidor_deformed_vertexes) == len(pp_deformed_vertexes) == len(pp_ort_deformed_vertexes)== len(rbf_deformed_vertexes), \
			f"Vertex count mismatch in files: {pp_sidor_file}, {pp_file}, {pp_ort_file}, {rbf_file}"

		# Compute mean squared errors
		mean_se_pp_sidor_rbf = mean_squared_error(pp_sidor_deformed_vertexes, rbf_deformed_vertexes)
		mean_se_pp_rbf = mean_squared_error(pp_ort_deformed_vertexes, rbf_deformed_vertexes)
		mean_se_pp_ort_rbf = mean_squared_error(pp_ort_deformed_vertexes, rbf_deformed_vertexes)

		# Add row to Excel
		params_name = all_pp_sidor_deformed[file_index].split('/')[-1]
		params_name = params_name.replace(pp_sidor_deformed_basename + '_', '').replace('.obj', '')
		sheet.append([params_name, mean_se_pp_sidor_rbf, mean_se_pp_rbf, mean_se_pp_ort_rbf])

	# Save Excel file
	excel_filepath = os.path.join(subdir, excel_filename)
	workbook.save(excel_filepath)
	print(f"Excel report generated: {excel_filepath}")


if __name__ == "__main__":
	# icosphere.obj screwed with tetraderal basis
	# root_dir = 'obj/results/article/screwed/'
 
	# pp_ort_tetr_13v_screwed_div_20_vs, un1_ts = parse_obj_file(root_dir + 'pp_ort_tetr_13v_screwed_div_20.obj')
	# pp_sidor_tetr_13v_screwed_div_20_vs, un2_ts = parse_obj_file(root_dir + 'pp_sidor_tetr_13v_screwed_div_20.obj')
	# pp_tetr_13v_screwed_div_20_vs, un3_ts = parse_obj_file(root_dir + 'pp_tetr_13v_screwed_div_20.obj')
	# rbf_tetr_13v_screwed_div_20_vs, un4_ts = parse_obj_file(root_dir + 'rbf_tetr_13v_screwed_div_20.obj')
 
	# mean_se_2_rbf = mean_squared_error(pp_sidor_tetr_13v_screwed_div_20_vs, rbf_tetr_13v_screwed_div_20_vs)
	# mean_se_3_rbf = mean_squared_error(pp_tetr_13v_screwed_div_20_vs, rbf_tetr_13v_screwed_div_20_vs)
	# mean_se_1_rbf = mean_squared_error(pp_ort_tetr_13v_screwed_div_20_vs, rbf_tetr_13v_screwed_div_20_vs)
	# print(mean_se_1_rbf, mean_se_2_rbf, mean_se_3_rbf)
 
	# exit(0)
 
	root_dir = 'obj/results/article'

	generate_deformed_report(
		subdir = os.path.join(root_dir, 'waved/'),
		pp_sidor_deformed_basename='pp_sidor_tetr_13v_waved',
		pp_ort_deformed_basename='pp_ort_tetr_13v_waved',
		pp_deformed_basename='pp_tetr_13v_waved',
		rbf_deformed_basename='rbf_tetr_13v_waved',
		excel_filename='wave_deformation_report_2.xlsx'
	)
	# generate_deformed_report(
	# 	subdir = os.path.join(root_dir, 'screwed/'),
	# 	script_deformed_basename='bunny_1_screwed',
	# 	rbf_deformed_basename='result_rbf_deformed_1_screwed',
	# 	pp_deformed_basename='result_pp_deformed_1_screwed',
	# 	excel_filename='screw_deformation_report_2.xlsx'
	# )
	# generate_deformed_report(
	# 	subdir = os.path.join(root_dir, 'squared/'),
	# 	script_deformed_basename='bunny_1_squared',
	# 	rbf_deformed_basename='result_rbf_deformed_1_squared',
	# 	pp_deformed_basename='result_pp_deformed_1_squared',
	# 	excel_filename='squared_deformation_report_2.xlsx'
	# )
