import numpy as np
import simple_draw as sd

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


def envelope_box_count(points):  # np vertex array
    xmax = np.max(points[:, 0])
    ymax = np.max(points[:, 1])
    zmax = np.max(points[:, 2])
    xmin = np.min(points[:, 0])
    ymin = np.min(points[:, 1])
    zmin = np.min(points[:, 2])
    return xmin, ymin, zmin, xmax, ymax, zmax


def focuse_point_count(points):  # np vertex array
    xmin, ymin, zmin, xmax, ymax, zmax = envelope_box_count(points)
    x = (xmax + xmin) / 2
    y = (ymax + ymin) / 2
    z = (zmax + zmin) / 2
    return x, y, z


if __name__ == '__main__':
    stlFile = 'LK1-002.01c.STL'
    model = model_create(stlFile)
    vertex = model.get_vxs_np_array()
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
    print(vertex)
    print(envelope_box_count(vertex))
    print((focuse_point_count(vertex)))
    sd._init()
