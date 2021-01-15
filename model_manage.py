import argparse

import numpy as np
import simple_draw as sd

import data_def as dd
import file_read as fr
import vertex_manipulations as vm

X = 0
Y = 1
Z = 2
R = 0
A = 1
E = 2
Q = 3

def main():
    parser = parserDefinition()
    args = parser.parse_args()
    xResolution = args.xres
    yResolution = args.yres
    sd.resolution = (xResolution, yResolution)
    xCenter = xResolution / 2
    yCenter = yResolution / 2
    stlFile: str = args.file.name  # 'LK1-002.01c.STL'
    fileType = stlFile[-3:].upper()
    print(stlFile, fileType)
    if fileType == 'PKL':
        model = fr.pickleRead(stlFile)
    else:
        picklFile = stlFile + '.pkl'
        # print(stlFile, picklFile, fileType)
        model = model_create(stlFile)
        fr.pickleWrite(picklFile, model)
    vertex = model.get_vxs_np_array()
    bodyCenter = vm.body_center_count(vertex)
    print(bodyCenter)
    vxsXYZcentered = vm.array_plus_point(pts=vertex,
                                         pt=(-bodyCenter[X], -bodyCenter[Y], -bodyCenter[Z]))
    vxsDAEbodyCenter = vm.arrayXYZtoDAE(vxsXYZcentered)
    deltaA = 00  # degrees
    deltaE = 00  # degrees
    scale = 10
    currentBodyVxsDAE = vm.array_plus_point(pts=vxsDAEbodyCenter,
                                            pt=(0, np.radians(deltaA), np.radians(deltaE)))
    # currentBodyVxsDAE = vxsDAEbodyCenter
    screenProjectionVXsXYZ = np.round(vm.arrayDAEtoXYZ(currentBodyVxsDAE))
    # screenProjectionVXsXYZ = vertex
    envBox = vm.envelope_box_count(screenProjectionVXsXYZ)
    print(envBox)
    screenProjectionVXsXYZ = np.multiply(screenProjectionVXsXYZ, scale)
    screenProjectionVXsXYZ = vm.array_plus_point(pts=screenProjectionVXsXYZ,
                                                 pt=(xCenter, yCenter, 0))
    envBox = vm.envelope_box_count(screenProjectionVXsXYZ)
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
