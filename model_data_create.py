import data_def as dd
import file_read as fr


def model_create(name: str) -> dd.BodyFaces:
    """Reads STL model data and creates data structures.
    :returns model data structure"""

    body = dd.BodyFaces()
    sourceFile = fr.stl_reader(filename=name)
    faces = iter(sourceFile)
    for faceVXses in faces:
        body.add_face(facePoints=faceVXses)
    return body


if __name__ == '__main__':
    stlFile = 'LK1-002.01c.STL'
    model = model_create(stlFile)
    # print(len(model))
    # print(model.get_vxs_np_array())
    # print(model.get_all_edges())
    # print(model.get_edges_list())
    # print(model.get_vertex_list())
    print(model.get_centerXYZ())
    for i in range(len(model)):
        print(i)
        print(model.get_face_edges(i))
        print(model.get_face_vertexes(i))