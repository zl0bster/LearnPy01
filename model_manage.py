import argparse
from typing import Sequence

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


def main():
    parser = parserDefinition()
    args = parser.parse_args()
    xResolution = args.xres
    yResolution = args.yres
    sd.resolution = (xResolution, yResolution)
    xCenter = xResolution / 2
    yCenter = yResolution / 2
    stlFile = args.file.name  # 'LK1-002.01c.STL'
    model = model_create(stlFile)
    vertex = model.get_vxs_np_array()
    bodyCenter = focuse_point_count(vertex)
    print(bodyCenter)
    vxsXYZcentered = array_plus_point(pts=vertex,
                                      pt=(-bodyCenter[X], -bodyCenter[Y], -bodyCenter[Z]))
    vxsDAEbodyCenter = arrayXYZtoDAE(vxsXYZcentered)
    deltaA = 00  # degrees
    deltaE = 00  # degrees
    scale = 10
    currentBodyVxsDAE = array_plus_point(pts=vxsDAEbodyCenter,
                                         pt=(0, np.radians(deltaA), np.radians(deltaE)))
    # currentBodyVxsDAE = vxsDAEbodyCenter
    screenProjectionVXsXYZ = np.round(arrayDAEtoXYZ(currentBodyVxsDAE))
    screenProjectionVXsXYZ = vertex
    envBox = envelope_box_count(screenProjectionVXsXYZ)
    print(envBox)
    screenProjectionVXsXYZ = np.multiply(screenProjectionVXsXYZ, scale)
    screenProjectionVXsXYZ = array_plus_point(pts=screenProjectionVXsXYZ,
                                              pt=(xCenter, yCenter, 0))
    envBox = envelope_box_count(screenProjectionVXsXYZ)
    print(envBox)
    sd._init()
    draw_model_1(model=model, screenVXs=screenProjectionVXsXYZ)
    while not sd.user_want_exit():
        continue
    sd.quit()


def parserDefinition():
    """
    command line arguments parse to adjust screen object parameters
    :return:
    parser data structure
    screen resolution
    parser.xres : int  - screen resolution
    parser.yres : int  - screen resolution
    parser.file : str  - configuration file name
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xres', help='window x resolution', type=int, default=1600)
    parser.add_argument('-y', '--yres', help='window y resolution', type=int, default=950)
    parser.add_argument('-file', type=argparse.FileType('r'), help='scene config file path', required=True)
    return parser


def draw_model_1(model: dd.BodyFaces, screenVXs):
    edgesList = model.get_all_edges()
    sd.start_drawing()  # removes  blinking
    for edge in edgesList:
        pt1 = sd.get_point(screenVXs[edge[0], X], screenVXs[edge[0], Y])
        pt2 = sd.get_point(screenVXs[edge[1], X], screenVXs[edge[1], Y])
        sd.line(pt1, pt2)
    sd.finish_drawing()  # removes  blinking


def model_create(name: str) -> dd.BodyFaces:
    """Reads STL model data and creates data structures.
    :returns model data structure"""

    body = dd.BodyFaces()
    sourceFile = fr.stl_reader_2(filename=name)
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
    xmin = abs(xmin) if xmin < 0 else -xmin
    ymin = abs(ymin) if ymin < 0 else -ymin
    zmin = abs(zmin) if zmin < 0 else -zmin
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


def pointsXYZdelta(pnt1: Sequence[float], pnt2: Sequence[float]) -> Sequence[float]:
    x = pnt2[X] - pnt1[X]
    y = pnt2[Y] - pnt1[Y]
    z = pnt2[Z] - pnt1[Z]
    return x, y, z


def array_plus_point(pts, pt: Sequence[float]):  # np vertex array in XYZ or DAE
    """Transforms decart coordinates array to angular"""
    result = np.zeros(pts.shape)
    for i in range(pts.shape[0]):
        result[i, X] = pts[i, X] + pt[X]
        result[i, Y] = pts[i, Y] + pt[Y]
        result[i, Z] = pts[i, Z] + pt[Z]
    return result


if __name__ == '__main__':
    # stlFile = 'LK1-002.01c.STL'
    # model = model_create(stlFile)
    # vertex = model.get_vxs_np_array()
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
    # print(vertex)
    # print(envelope_box_count(vertex))
    # print((focuse_point_count(vertex)))

    # print(vertex.shape[0])
    # print(vertex.size)
    # for i in range(vertex.shape[0]):
    #     print(vertex[i])
    # vxDAE = arrayXYZtoDAE(vertex)
    # # print(np.subtract(vertex, arrayDAEtoXYZ(vxDAE)))
    # print(array_plus_point(pts=vertex, pt=(10, -10, 10)))
    main()
