import os
from openpyxl import Workbook
import numpy as np
from RBF_exosceleton.obj_io import vertexes  # Assuming this function parses OBJ data

def list_files(directory, startswith, extension):
	"""List files in a directory that start with a given string and have a given extension."""
	return [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if f.startswith(startswith) and f.endswith('.' + extension)]

def mean_squared_error(vertices1, vertices2):
	"""Compute the mean squared error between two sets of vertices."""
	vertices1 = np.array(vertices1)
	vertices2 = np.array(vertices2)
	return np.square(np.subtract(vertices1, vertices2)).mean()

def generate_deformed_report(subdir, script_deformed_basename, rbf_deformed_basename, pp_deformed_basename, excel_filename):

	all_script_deformed = list_files(subdir, script_deformed_basename, 'obj')
	all_rbf_deformed = list_files(subdir, rbf_deformed_basename, 'obj')
	all_pp_deformed = list_files(subdir, pp_deformed_basename, 'obj')
	
	assert len(all_script_deformed) == len(all_rbf_deformed) == len(all_pp_deformed), "Mismatch in file counts!"

	# Create Excel workbook
	workbook = Workbook()
	sheet = workbook.active
	sheet.title = f"{(excel_filename.split('.')[0]).replace('_', ' ')}"

	# Write header
	sheet.append(['Params', 'Script-RBF MSE', 'Script-PP MSE', 'RBF-PP MSE'])

	for file_index, (script_file, rbf_file, pp_file) in enumerate(zip(all_script_deformed, all_rbf_deformed, all_pp_deformed)):
		with open(script_file, 'r') as f:
			script_deformed_vertexes = vertexes(f.read())
		with open(rbf_file, 'r') as f:
			rbf_deformed_vertexes = vertexes(f.read())
		with open(pp_file, 'r') as f:
			pp_deformed_vertexes = vertexes(f.read())

		assert len(script_deformed_vertexes) == len(rbf_deformed_vertexes) == len(pp_deformed_vertexes), \
			f"Vertex count mismatch in files: {script_file}, {rbf_file}, {pp_file}"

		# Compute mean squared errors
		mean_se_script_rbf = mean_squared_error(script_deformed_vertexes, rbf_deformed_vertexes)
		mean_se_script_pp = mean_squared_error(script_deformed_vertexes, pp_deformed_vertexes)
		mean_se_rbf_pp = mean_squared_error(rbf_deformed_vertexes, pp_deformed_vertexes)

		# Add row to Excel
		params_name = all_script_deformed[file_index].split('/')[-1]
		params_name = params_name.replace(script_deformed_basename + '_', '').replace('.obj', '')
		sheet.append([params_name, mean_se_script_rbf, mean_se_script_pp, mean_se_rbf_pp])

	# Save Excel file
	excel_filepath = os.path.join(subdir, excel_filename)
	workbook.save(excel_filepath)
	print(f"Excel report generated: {excel_filepath}")


if __name__ == "__main__":
	root_dir = 'obj/results/'

	generate_deformed_report(
		subdir = os.path.join(root_dir, 'waved/'),
		script_deformed_basename='bunny_1_waved',
		rbf_deformed_basename='result_rbf_deformed_1_waved',
		pp_deformed_basename='result_pp_deformed_1_waved',
		excel_filename='wave_deformation_report_2.xlsx'
	)
	generate_deformed_report(
		subdir = os.path.join(root_dir, 'screwed/'),
		script_deformed_basename='bunny_1_screwed',
		rbf_deformed_basename='result_rbf_deformed_1_screwed',
		pp_deformed_basename='result_pp_deformed_1_screwed',
		excel_filename='screw_deformation_report_2.xlsx'
	)
	generate_deformed_report(
		subdir = os.path.join(root_dir, 'squared/'),
		script_deformed_basename='bunny_1_squared',
		rbf_deformed_basename='result_rbf_deformed_1_squared',
		pp_deformed_basename='result_pp_deformed_1_squared',
		excel_filename='squared_deformation_report_2.xlsx'
	)
