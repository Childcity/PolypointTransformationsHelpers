import os
from openpyxl import Workbook
import numpy as np
from RBF_exosceleton.obj_io import *

def list_files(directory, startswith, extension):
	"""List files in a directory that start with a given string and have a given extension."""
	return [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if f.startswith(startswith) and f.endswith('.' + extension)]

def count_rmse(expected, actual):
	expected = np.array(expected)
	actual = np.array(actual)
	square_diff = (expected - actual) ** 2
	mse = np.mean(square_diff, axis=0)
	return np.sqrt(mse) # returns [RMSEx, RMSEy, RMSEz]

def count_normilized_rmse(expected, actual):
	rmse = count_rmse(expected, actual)
	norm_value = np.max(expected, axis=0) - np.min(expected, axis=0)
	#norm_value = expected.mean()
	return rmse / norm_value # returns [RMSEx, RMSEy, RMSEz]

def generate_deformed_report(subdir, methods_deformed_basename, ethalon_deformed_basename, excel_filename):

	all_files_for_method = dict()
	for method_basename in methods_deformed_basename:
		all_files_for_method[method_basename] = list_files(subdir, method_basename, 'obj')
	all_files_for_ethalon_method = list_files(subdir, ethalon_deformed_basename, 'obj')

	for method_basename, files in all_files_for_method.items():
		eth_len = len(all_files_for_ethalon_method)
		files_len = len(files)
		assert eth_len == files_len, f"Mismatch in file counts! {eth_len} != {files_len}"

	# Create Excel workbook
	workbook = Workbook()
	sheet = workbook.active
	sheet.title = f"{(excel_filename.split('.')[0]).replace('_', ' ')}"

	# Write header
	sheet.append(['Params'] + ['MSE ' + method_basename for method_basename in methods_deformed_basename])

	for file_index, ethalon_method_file_path in enumerate(all_files_for_ethalon_method):
		print(f"Processing file {file_index + 1}/{len(all_files_for_ethalon_method)}")
  
		deformed_vertexes = dict()
		for method_basename, files in all_files_for_method.items():
			deformed_vertexes[method_basename], _ = parse_obj_file(files[file_index])
		ethalon_deformed_vertexes, _ = parse_obj_file(ethalon_method_file_path)
  
		for method_basename, verts in deformed_vertexes.items():
			assert len(verts) == len(ethalon_deformed_vertexes), f"Vertex count mismatch: {len(verts)} != {len(ethalon_deformed_vertexes)}"

		# Compute mean squared errors
		rmse = [
      			round(count_rmse(ethalon_deformed_vertexes, verts).mean(), 2)
         			for verts in deformed_vertexes.values()
             ]

		# Add row to Excel
		params_name = ethalon_method_file_path.split('/')[-1]
		params_name = params_name.replace(ethalon_deformed_basename + '_', '').replace('.obj', '')
		sheet.append([params_name] + rmse)

	# Save Excel file
	excel_filepath = os.path.join(subdir, excel_filename)
	workbook.save(excel_filepath)
	print(f"Excel report generated: {excel_filepath}")


if __name__ == "__main__":
 
	root_dir = 'obj/results/article'

	generate_deformed_report(
		subdir = os.path.join(root_dir, 'radial_scale/'),
		methods_deformed_basename=['pp_sidor_cube_1_radial_scale', 'pp_ort_cube_1_radial_scale', 'pp_cube_1_radial_scale', 'rbf_cube_1_radial_scale'],
		ethalon_deformed_basename='thorus_480v_radial_scale',
		excel_filename='wave_deformation_report_2.xlsx'
	)
 
	# generate_deformed_report(
	# 	subdir = os.path.join(root_dir, 'screwed/'),
	# 	methods_deformed_basename=['pp_sidor_cube_1_screwed', 'pp_ort_cube_1_screwed', 'pp_cube_1_screwed', 'rbf_cube_1_screwed'],
	# 	ethalon_deformed_basename='thorus_480v_screwed',
	# 	excel_filename='screw_deformation_report_2.xlsx'
	# )
	# generate_deformed_report(
	# 	subdir = os.path.join(root_dir, 'squared/'),
	# 	script_deformed_basename='bunny_1_squared',
	# 	rbf_deformed_basename='result_rbf_deformed_1_squared',
	# 	pp_deformed_basename='result_pp_deformed_1_squared',
	# 	excel_filename='squared_deformation_report_2.xlsx'
	# )
