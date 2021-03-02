from enum import Enum
from typing import Sequence  # , Any, Optional

import numpy as np
import pygame as pg
import simple_draw as sd
from loguru import logger

import data_def as dd
import vertex_manipulations as vm

"""this module contains classes for model display mode definition"""
X = 0
Y = 1
Z = 2
DEBUG = 0


class DispModes(Enum):
    wireFrame = 1
    flatsHidden = 2
    rearSurfHidden = 3


# class SurfAttr(Enum):


class DisplayModel:
    """
    ---turn model
    ---rescale model
    ---calc model pos
    ---draw model
    input screen parameters
    to manage all model data inside class"""

    def __init__(self, modelData: dd.BodyFaces, screen: Sequence[int]):
        self.model = modelData
        self.displayMode = DispModes.flatsHidden
        self.edgesList1 = self.model.get_unique_edges()
        self.baseVXsCoords = self.model.get_vxs_np_array()
        self.countVXCoords = self.baseVXsCoords
        self.screenResolution = screen
        self.bodyCenter = vm.body_center_count(self.baseVXsCoords)
        print(self.bodyCenter)
        self.baseVXsCoords = vm.array_plus_point(pts=self.baseVXsCoords,
                                                 pt=(-self.bodyCenter[X], -self.bodyCenter[Y], -self.bodyCenter[Z]))
        self.model.set_scale(10)
        self.model.set_normal((0, 0, 0))
        self.screen = None
        self.currentFCsNormal = self._count_fcs_normals(faces=self.model.get_all_faces())
        self._mark_flat_edges()
        self.edgesList2 = self.get_non_flat_edges()
        logger.debug(f"""       counted:
                faces: {len(self.model.faces)}
                edges: {len(self.model.edges)}
                flats: {len(self.model.edges.isFlat)}""")
        logger.debug(self.currentFCsNormal)
        # if DEBUG:
        #     # print(self.model.get_all_faces())
        #     print(self.currentFCsNormal)
        #     # print(self.model.edges.isFlat)
        #     print(f"""       counted:
        #         faces: {len(self.model.faces)}
        #         edges: {len(self.model.edges)}
        #         flats: {len(self.model.edges.isFlat)}""")
        # TODO initialize surface analize

    def set_display_mode(self, mode: DispModes):
        self.displayMode = mode

    def set_screen(self, screen: pg.display):
        self.screen = screen
        sd.take_background()

    def get_edges(self) -> Sequence[int]:
        """returns list of edges to display for different display modes"""
        if self.displayMode == DispModes.flatsHidden:
            return self.edgesList2
        else:
            return self.edgesList1

    def get_non_flat_edges(self):
        """fills the list with edges numbers which are not between parallel surfaces"""
        nonFlatEdgesToShow = []
        for i, edge in enumerate(self.model.edges):
            logger.debug(i, self.model.edges.get_flattness(i), edge)
            # if DEBUG:
            #     print(i, self.model.edges.get_flattness(i), edge)
            if not self.model.edges.get_flattness(i):
                nonFlatEdgesToShow.append(edge)
        return nonFlatEdgesToShow

    # def get_surfaces(self) -> Sequence[int]:
    #     """returns list of surfaces to display"""
    #     ...

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
        """ turns vertexes around 3 axis'
        shifts vertexes to origin in center of screen"""
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

    def _count_fcs_normals(self, faces: Sequence[dd.Face]):
        """ for each surface provides nparray with coords of 3 vertexes
        and counts normal vector coords to add to the result list"""
        result = []
        for i, face in enumerate(faces):
            dd.progress_show(f"normal for face : {i} ")
            vxsList = list(face.get_vertexes())
            vxcMatrix = vm.make_surf_MX_from_VX_array(vxs=self.countVXCoords, pts=vxsList)
            result.append(vm.count_norm_to_surf(vxcMatrix))
        return np.array(result)

    def _mark_flat_edges(self):
        """compares normal vectors of neighbour surfaces
        to check if they are colinear (faces are paralell, edge is flat)"""
        nonPairedEdges = 0
        for edge in range(len(self.model.edges)):
            surface1 = self.model.edges.get_edges_surf(edge)
            if self.model.edges.get_edge_colinear(edge):
                surface2 = self.model.edges.get_edge_colinear(edge)[0]
                surface2 = surface2 if surface2 else 0
                surface2 = self.model.edges.get_edges_surf(surface2)
                normVec1 = np.array(self.currentFCsNormal[surface1])
                normVec2 = np.array(self.currentFCsNormal[surface2])
                deltaNorm = np.max(np.abs(normVec2 - normVec1))
                isFlat = (deltaNorm <= 0.02)
                logger.debug(f"""edge {edge} between {surface1} and {surface2}
                  {normVec1} and {normVec2}
                  delta: {deltaNorm} and found flat: {isFlat}""")
                # if DEBUG:
                #     print(f"edge {edge} between {surface1} and {surface2}")
                #     print(f"  {normVec1} and {normVec2}")
                #     print(f"  delta: {deltaNorm} and found flat: {isFlat}")
            else:
                isFlat = False
                nonPairedEdges += 1
            self.model.edges.set_flattness(val=isFlat)
        logger.debug(f"""total edges count: {len(self.model.edges)}
            unique edges count: {len(self.edgesList1)}
            edges without pair: {nonPairedEdges}""")
        # if DEBUG:
        #     print("+ " * 10)
        #     print(f'total edges count: {len(self.model.edges)}')
        #     print(f'unique edges count: {len(self.edgesList1)}')
        #     # print(f'nonflat edges count: {len(self.edgesList2)}')
        #     print(f'edges without pair: {nonPairedEdges}')
        #     print("+ " * 10)


#     class Surfaces:
#         """should define attributes if surface:
#         belongs to any sort of special kind (flat or cilinder) and to which face it belongs
#         orientation - +Z or -Z
#         which simple surface are its neighbours
#         """
#
#         def __init__(self):
#             # TODO get surfaces data from model
#             self.facesNormals = self._count_fcs_normals()
#             # TODO form flat surfaces on triangles
#             ...
#
#         def __faces_normal_count(self) -> np.array:
#             ...
#
#
# class Edges():
#
#     def __init__(self):
#         # TODO find collinear edge to each edge
#         ...

logger.add('body_display.log', rotation='1 MB')
logger.level("DEBUG")
