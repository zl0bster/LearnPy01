import argparse
import sys

import numpy as np
import pygame as pg
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

    def turn_model(ax: int = 0, ay: int = 0, az: int = 0, ):
        bodyOrientation = list(model.get_normal())
        if ax:
            bodyOrientation[X] += np.radians(ax)
            bodyOrientation[X] = vm.shift2pi_correction(bodyOrientation[X])
        if ay:
            bodyOrientation[Y] += np.radians(ay)
            bodyOrientation[Y] = vm.shift2pi_correction(bodyOrientation[Y])
        if az:
            bodyOrientation[Z] += np.radians(az)
            bodyOrientation[Z] = vm.shift2pi_correction(bodyOrientation[Z])
        model.set_normal(tuple(bodyOrientation))

    # def turn_model_1(a: int = 0, e: int = 0):  # azimuth and elevation angles are in degrees
    #     bodyOrientation = list(model.get_normal())
    #     print('*' * 20)
    #     print(bodyOrientation)
    #     print(a, e)
    #     if a:
    #         bodyOrientation[A] += np.radians(a)
    #         if bodyOrientation[A] > np.pi:
    #             bodyOrientation[A] = -2 * np.pi + bodyOrientation[A]
    #         if bodyOrientation[A] < -np.pi:
    #             bodyOrientation[A] = 2 * np.pi + bodyOrientation[A]
    #     if e:
    #         bodyOrientation[E] += np.radians(e)
    #         if bodyOrientation[E] > np.pi:
    #             bodyOrientation[E] = -2 * np.pi + bodyOrientation[E]
    #         if bodyOrientation[E] < -np.pi:
    #             bodyOrientation[E] = 2 * np.pi + bodyOrientation[E]
    #     # print(bodyOrientation)
    #     model.set_normal(tuple(bodyOrientation))

    def rescale(z: float = 1.0):
        model.set_scale(z * model.get_scale())

    def read_button():
        keyTable = {"UP": [pg.K_UP, turn_model, {'ax': 10}],
                    "DN": [pg.K_DOWN, turn_model, {'ax': -10}],
                    "LT": [pg.K_LEFT, turn_model, {'ay': 10}],
                    "RT": [pg.K_RIGHT, turn_model, {'ay': -10}],
                    "CW": [pg.K_PAGEUP, turn_model, {'az': 10}],
                    "СС": [pg.K_PAGEDOWN, turn_model, {'az': -10}],
                    "ZI": [pg.K_LSHIFT, rescale, {'z': 1.1}],
                    "ZO": [pg.K_LCTRL, rescale, {'z': 0.9}],
                    }
        while True:
            if sd.user_want_exit():
                sd.quit()
            for evnt in pg.event.get():
                if evnt.type == pg.QUIT:
                    # sd.quit()
                    sys.exit()
                elif evnt.type == pg.KEYDOWN:
                    for keyAction in keyTable.values():
                        checkKey = keyAction[0]
                        keyFx = keyAction[1]
                        fxArgs = keyAction[2]
                        if evnt.key == checkKey:
                            keyFx(**fxArgs)
                            return

    def calc_model_pos():
        orientation = list(model.get_normal())
        ax = orientation[X]
        ay = orientation[Y]
        az = orientation[Z]
        currentBodyVxsXYZ = np.multiply(vxsXYZcentered, model.get_scale())
        currentBodyVxsXYZ = vm.arrayXYZrotX(pts=currentBodyVxsXYZ, a=ax)
        currentBodyVxsXYZ = vm.arrayXYZrotY(pts=currentBodyVxsXYZ, a=ay)
        currentBodyVxsXYZ = vm.arrayXYZrotZ(pts=currentBodyVxsXYZ, a=az)
        currentBodyVxsXYZ = vm.array_plus_point(pts=currentBodyVxsXYZ,
                                                pt=(xCenter, yCenter, 0))
        return currentBodyVxsXYZ


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
        model = model_create(stlFile)
        fr.pickleWrite(picklFile, model)
    vertex = model.get_vxs_np_array()
    bodyCenter = vm.body_center_count(vertex)
    print(bodyCenter)
    vxsXYZcentered = vm.array_plus_point(pts=vertex,
                                         pt=(-bodyCenter[X], -bodyCenter[Y], -bodyCenter[Z]))
    model.set_scale(10)
    model.set_normal((0, 0, 0))
    sd._init()
    sd.take_background()
    while not sd.user_want_exit():
        draw_model_1(model=model, screenVXs=calc_model_pos())
        read_button()


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
    sd.draw_background()
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
    # read_button()
    main()
