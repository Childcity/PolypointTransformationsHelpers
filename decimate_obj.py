import pymeshlab

# for filter_name in pymeshlab.filter_list():
#     print(filter_name)

def decimate(reduce_factor = 50): # %
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh('./obj/bunny/bunny_1.obj')

    m = ms.current_mesh()
    print('Input mesh has', m.vertex_number(), 'vertex and', m.face_number(), 'faces')

    target_faces = int(m.face_number() * (reduce_factor / 100))
    ms.apply_filter('meshing_decimation_quadric_edge_collapse',
                    targetfacenum=target_faces,
                    qualitythr=0.5,
                    preservenormal=True,
                    preservetopology=True)
    print('Output mesh has', m.vertex_number(), 'vertex and', m.face_number(), 'faces')

    # Save the simplified model
    ms.save_current_mesh(f"bunny_decimated_{reduce_factor}.obj")

if __name__ == "__main__":
	for i in range(10, 100, 10):
		decimate(i)
		print('decimated with', i, '%')