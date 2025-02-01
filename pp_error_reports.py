import os
from openpyxl import Workbook
import numpy as np
from RBF_exosceleton.obj_io import *

def adjust_column_width(sheet):
	for col in sheet.columns:
		max_length = 0
		column = col[0].column_letter # Get the column name
		for cell in col:
			try:
				if len(str(cell.value)) > max_length:
					max_length = len(cell.value)
			except:
				pass
		adjusted_width = (max_length + 2)
		sheet.column_dimensions[column].width = adjusted_width

def list_files(directory, startswith, extension):
	"""List files in a directory that start with a given string and have a given extension, sorted by date."""
	files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith(startswith) and f.endswith('.' + extension)]
	files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
	return files

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
  
	sheet_data1 = []
	sheet_data2 = []
 
	# Write header
	sheet_data1.append(['Params'] + ['RMSE ' + method_basename for method_basename in methods_deformed_basename])
	sheet_data2.append(['Params'] + ['TIME ' + method_basename for method_basename in methods_deformed_basename])

	for file_index, ethalon_method_file_path in enumerate(all_files_for_ethalon_method):
		print(f"Processing file {file_index + 1}/{len(all_files_for_ethalon_method)}")
  
		deformed_vertexes = dict()
		deformed_vertexes_elapsed_time = dict()
		for method_basename, files in all_files_for_method.items():
			deformed_vertexes[method_basename], _ = parse_obj_file(files[file_index])
			deformed_vertexes_elapsed_time[method_basename] = parse_elapsed_time(files[file_index])
		ethalon_deformed_vertexes, _ = parse_obj_file(ethalon_method_file_path)
  
		for method_basename, verts in deformed_vertexes.items():
			assert len(verts) == len(ethalon_deformed_vertexes), f"Vertex count mismatch: {len(verts)} != {len(ethalon_deformed_vertexes)}"

		# Compute mean squared errors
		rmse = [
      			round(count_rmse(ethalon_deformed_vertexes, verts).mean(), 2)
         			for verts in deformed_vertexes.values()
             ]
		elapsed_time = [ time for time in deformed_vertexes_elapsed_time.values() ]

		# Add row to Excel
		params_name = ethalon_method_file_path.split('/')[-1]
		params_name = params_name.replace(ethalon_deformed_basename + '_', '').replace('.obj', '')
		sheet_data1.append([params_name] + rmse)
		sheet_data2.append([params_name] + elapsed_time)

	# Save Excel file
	for row in sheet_data1 + [['']] + sheet_data2:
		sheet.append(row)
	adjust_column_width(sheet)
	excel_filepath = os.path.join(subdir, excel_filename)
	workbook.save(excel_filepath)
	print(f"Excel report generated: {excel_filepath}")


if __name__ == "__main__":
 
	root_dir = 'obj/results/article'
 
	generate_deformed_report(
		subdir = os.path.join(root_dir, 'screwed_1_16/'),
		methods_deformed_basename=[
      		'pp_sidor_cube_2_screwed', 'pp_ort_cube_2_screwed',
        	'pp_intr_cube_2_screwed', 'rbf_cube_2_screwed'
        ],
		ethalon_deformed_basename='torus_156v_screwed',
		excel_filename='screwed_1_16_deformation_report.xlsx'
	)

	# generate_deformed_report(
	# 	subdir = os.path.join(root_dir, 'mul_01_10/'),
	# 	methods_deformed_basename=[
    #   		'pp_sidor_cube_2', 'pp_ort_cube_2',
    #     	'pp_intr_cube_2', 'rbf_cube_2'
    #     ],
	# 	ethalon_deformed_basename='torus_156v',
	# 	excel_filename='mul_01_10_deformation_report.xlsx'
	# )
 
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
