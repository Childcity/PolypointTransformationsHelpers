def _list_by_prefix(prefix, text, to_type = lambda x: float(x) ):
	ls = []
	for line in text.split('\n'):
		if line.startswith(prefix):
			line = line[len(prefix):].strip()
			ls += [[to_type(l.replace(',', '.')) for l in line.split(' ')]]
	return ls
	

def _str_by_prefix(prefix, elements):
	st = ""
	for line_el in elements:
		st += prefix
		for el in line_el:
			st += ' ' + str(el)
		st += '\n'
	return st


#v 4,875346 21,185596 0,000000
def vertexes(text):
	return _list_by_prefix('v ', text)

def normals(text):
	return _list_by_prefix('vn ', text)

#f 1/x/x 2/x/x 3/x/x
# Returns list, each element is a list of 3 indices of vertices
def triangles(text):
	return _list_by_prefix('f ', text, lambda s: int(s.split('/')[0]))

#f x/x/1 x/x/2 x/x/3
def triangle_normals(text):
	return _list_by_prefix('f ', text, lambda s: int(s.split('/')[2]))

def triangle_point(vertexes, triangle_indx):
	return [
		vertexes[triangle_indx - 1][0], # X
		vertexes[triangle_indx - 1][1], # Y
		vertexes[triangle_indx - 1][2], # Z
	]

def parse_obj_file(file_path: str) -> tuple[list[float], list[float]]:
	with open(file_path, 'r') as f:
		obj = f.read()
		return vertexes(obj), triangles(obj)
	assert False

def parse_elapsed_time(file_path: str) -> tuple[list[float], list[float]]:
	with open(file_path, 'r') as f:
		obj = f.read()
		return _list_by_prefix('# elapsed_time: ', obj)[0][0]
	assert False

# output
def str_from_vertexes(vertexes):
	return _str_by_prefix('v', vertexes)

def str_from_faces(faces):
	return _str_by_prefix('f', faces)

if __name__ == "__main__":
	f = open('ellipsoid.obj', 'r')
	for vs in vertexes(f.read()):
		print ('v', vs)
	f.close()
	f = open('ellipsoid.obj', 'r')
	for tr in triangles(f.read()):
		print ('tr', tr)
	f.close()

