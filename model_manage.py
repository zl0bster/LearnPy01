import argparse
import sys

import numpy as np
import pygame as pg
import simple_draw as sd

import body_display as bd
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
                    #TODO ctrl+Z function with log
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
                            #TODO comand log for ctrl+z
                            return


    def print_data():
        f1 = pg.font.Font(None, 18)
        txtpos = (10, 20)
        orientation = model.get_normal()
        lines = [f'Model: {stlFile}',
                 f'Surfaces: {len(model)}',
                 "",
                 "Use arrow keys and PG_UP/PG_DN to turn model",
                 "Left SHIFT/CTRL to zoom in/out",
                 "",
                 f'Scale: {int(model.get_scale())}',
                 f'X angle:{int(np.degrees(orientation[X]))}',
                 f'Y angle:{int(np.degrees(orientation[Y]))}',
                 f'Z angle:{int(np.degrees(orientation[Z]))}'
                 ]
        for i, line in enumerate(lines):
            text1 = f1.render(line, True, sd.COLOR_DARK_YELLOW)
            sc.blit(text1, (txtpos[0], txtpos[1] + 20 * i))
        pg.display.update()

    parser = parserDefinition()
    args = parser.parse_args()
    xResolution = args.xres
    yResolution = args.yres
    sd.resolution = (xResolution, yResolution)
    stlFile: str = args.file.name  # 'LK1-002.01c.STL'
    fileType = stlFile[-3:].upper()
    print(stlFile, fileType)
    if fileType == 'PKL':
        model = fr.pickleRead(stlFile)
        savePKL = False
    else:
        picklFile = stlFile + '.pkl'
        model = model_create(stlFile)
        savePKL = True
    displayModel = bd.DisplayModel(modelData=model, screen=[xResolution, yResolution])
    if savePKL:
        fr.pickleWrite(picklFile, model)
    sd._init()
    pg.font.init()
    sc = pg.display.set_mode((xResolution, yResolution))
    sc.fill(sd.COLOR_DARK_BLUE)
    displayModel.set_screen(screen=sc)
    while not sd.user_want_exit():
        displayModel.draw_body()
        print_data()
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
    main()
