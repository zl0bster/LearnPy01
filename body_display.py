from enum import Enum
from typing import Sequence  # , Any, Optional

import numpy as np
import pygame as pg
import simple_draw as sd

import data_def as dd
import vertex_manipulations as vm

"""this module contains classes for model display mode definition"""
X = 0
Y = 1
Z = 2


class DispModes(Enum):
    wireFrame = 1
    flatsHidden = 2
    rearSurfHidden = 3


# class SurfAttr(Enum):


class DisplayModel:
    """TODO put here
    ---turn model
    ---rescale model
    calc model pos
    draw model
    inout screen parameters
    to manage all model data inside class"""

    def __init__(self, modelData: dd.BodyFaces, screen: Sequence[int]):
        self.model = modelData
        self.displayMode = DispModes.wireFrame
        self.edgesList1 = self.model.get_unique_edges()
        self.baseVXsCoords = self.model.get_vxs_np_array()
        self.countVXCoords = np.zeros_like(self.baseVXsCoords)
        self.screenResolution = screen
        self.bodyCenter = vm.body_center_count(self.baseVXsCoords)
        print(self.bodyCenter)
        self.baseVXsCoords = vm.array_plus_point(pts=self.baseVXsCoords,
                                                 pt=(-self.bodyCenter[X], -self.bodyCenter[Y], -self.bodyCenter[Z]))
        self.model.set_scale(10)
        self.model.set_normal((0, 0, 0))
        self.screen = None
        # TODO initialize surface analize

    def set_display_mode(self, mode: DispModes):
        self.displayMode = mode

    def set_screen(self, screen: pg.display):
        self.screen = screen
        sd.take_background()

    def get_edges(self) -> Sequence[int]:
        """returns list of edges to display"""
        return self.edgesList1

    def get_surfaces(self) -> Sequence[int]:
        """returns list of surfaces to display"""
        ...

    def draw_body(self):
        self._calc_current_model_pos()
        edgesList = self.get_edges()
        sd.start_drawing()  # removes  blinking
        sd.draw_background()
        for edge in edgesList:
            pt1 = sd.get_point(self.countVXCoords[edge[0], X], self.countVXCoords[edge[0], Y])
            pt2 = sd.get_point(self.countVXCoords[edge[1], X], self.countVXCoords[edge[1], Y])
            sd.line(pt1, pt2)
        sd.finish_drawing()  # removes  blinking

    def _calc_current_model_pos(self):
        orientation = list(self.model.get_normal())
        ax = orientation[X]
        ay = orientation[Y]
        az = orientation[Z]
        xCenter = self.screenResolution[X] // 2
        yCenter = self.screenResolution[Y] // 2
        currentBodyVxsXYZ = np.multiply(self.baseVXsCoords, self.model.get_scale())
        currentBodyVxsXYZ = vm.arrayXYZrotX(pts=currentBodyVxsXYZ, a=ax)
        currentBodyVxsXYZ = vm.arrayXYZrotY(pts=currentBodyVxsXYZ, a=ay)
        currentBodyVxsXYZ = vm.arrayXYZrotZ(pts=currentBodyVxsXYZ, a=az)
        currentBodyVxsXYZ = vm.array_plus_point(pts=currentBodyVxsXYZ,
                                                pt=(xCenter, yCenter, 0))
        self.countVXCoords = currentBodyVxsXYZ

    def _count_fcs_normals(self):
        result = []
        for face in self.model:
            vxsList = face.get_vertexes()
            vxcMatrix = vm.make_surf_MX_from_VX_array(pts=self.countVXCoords, vxs=vxsList)
            result.append(vm.count_norm_to_surf(vxcMatrix))
        return result


    class Surfaces:
        """should define attributes if surface:
        belongs to any sort of special kind (flat or cilinder) and to which face it belongs
        orientation - +Z or -Z
        which simple surface are its neighbours
        """

        def __init__(self):
            # TODO get surfaces data from model
            self.facesNormals = self._count_fcs_normals()
            # TODO form flat surfaces on triangles
            ...

        def __faces_normal_count(self) -> np.array:
            ...


class Edges():

    def __init__(self):
        # TODO find collinear edge to each edge
        ...
