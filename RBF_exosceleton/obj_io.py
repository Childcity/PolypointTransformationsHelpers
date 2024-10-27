def _list_by_prefix(prefix, text, to_type = lambda x: float(x) ):
	ls = []
	for line in text.split('\n'):
		if line.startswith(prefix):
			line = line[len(prefix):].strip()
			ls += [[to_type(l.replace(',', '.')) for l in line.split(' ')]]
	return ls
	

def _str_by_prefix(prefix, elements):
	st = ""
	for (a, b, c) in elements:
		st += prefix + str(a) + ' ' + str(b) + ' ' + str(c) + '\n'
	return st


#v 4,875346 21,185596 0,000000
def vertexes(text):
	return _list_by_prefix('v ', text)

def normals(text):
	return _list_by_prefix('vn ', text)

#f 1/x/x 2/x/x 3/x/x
def triangles(text):
	return _list_by_prefix('f ', text, lambda s: int(s.split('/')[0]))

def triangle_normals(text):
	return _list_by_prefix('f ', text, lambda s: int(s.split('/')[2]))

# output
def str_from_vertexes(vertexes):
	return _str_by_prefix('v ', vertexes)

def str_from_faces(faces):
	return _str_by_prefix('f ', faces)


if __name__ == "__main__":
	f = open('ellipsoid.obj', 'r')
	for vs in vertexes(f.read()):
		print ('v', vs)
	f.close()
	f = open('ellipsoid.obj', 'r')
	for tr in triangles(f.read()):
		print ('tr', tr)
	f.close()

