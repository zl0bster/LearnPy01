import numpy as np
import simple_draw as sd

import data_def as dd
import file_read as fr

X = 0
Y = 1
Z = 2
R = 0
A = 1
E = 2


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
    """Finds max and min coords in all axes to count envelope"""
    xmax = np.max(points[:, 0])
    ymax = np.max(points[:, 1])
    zmax = np.max(points[:, 2])
    xmin = np.min(points[:, 0])
    ymin = np.min(points[:, 1])
    zmin = np.min(points[:, 2])
    return xmin, ymin, zmin, xmax, ymax, zmax


def focuse_point_count(points):  # np vertex array
    """Counts center coord of envelope"""
    xmin, ymin, zmin, xmax, ymax, zmax = envelope_box_count(points)
    x = (xmax + xmin) / 2
    y = (ymax + ymin) / 2
    z = (zmax + zmin) / 2
    return x, y, z


def arrayXYZtoDAE(pts):  # np vertex array in XYZ
    """Transforms decart coordinates array to angular"""
    result = np.zeros(pts.shape)
    for i in range(pts.shape[0]):
        if pts[i].any() == 0:
            continue
        result[i, R] = np.sqrt(np.power(pts[i, X], 2) + np.power(pts[i, Y], 2) + np.power(pts[i, Z], 2))
        result[i, E] = np.arcsin(pts[i, Z] / result[i, R])
        lenXY = np.hypot(pts[i, X], pts[i, Y])
        if lenXY == 0:
            result[i, A] = np.pi / 2
        else:
            result[i, A] = np.arcsin(pts[i, Y] / lenXY)
    return result


def arrayDAEtoXYZ(pts):  # np vertex array in DAE
    """Transforms angular coordinates array to decart"""
    result = np.zeros(pts.shape)
    for i in range(pts.shape[0]):
        if pts[i].any() == 0:
            continue
        result[i, X] = pts[i, R] * np.cos(pts[i, E]) * np.cos(pts[i, A])
        result[i, Y] = pts[i, R] * np.cos(pts[i, E]) * np.sin(pts[i, A])
        result[i, Z] = pts[i, R] * np.sin(pts[i, E])
    return result


if __name__ == '__main__':
    stlFile = 'LK1-002.01c.STL'
    model = model_create(stlFile)
    vertex = model.get_vxs_np_array()
    # print(len(model))
    # print(model.get_vxs_np_array())
    # print(model.get_all_edges())
    # print(model.get_edges_list())
    # print(model.get_vertex_list())
    # print(model.get_centerXYZ())
    # for i in range(len(model)):
    #     print(i)
    #     print(model.get_face_edges(i))
    #     print(model.get_face_vertexes(i))
    print(vertex)
    # print(envelope_box_count(vertex))
    # print((focuse_point_count(vertex)))
    sd._init()
    print(vertex.shape[0])
    # print(vertex.size)
    # for i in range(vertex.shape[0]):
    #     print(vertex[i])
    vxDAE = arrayXYZtoDAE(vertex)
    print(np.subtract(vertex, arrayDAEtoXYZ(vxDAE)))
