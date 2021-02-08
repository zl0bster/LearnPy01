from typing import Sequence #, Any, Optional
import numpy as np
from enum import Enum

import data_def as dd
# import vertex_manipulations as vm

"""this module contains classes for model display mode definition"""


class DispModes(Enum):
    wireFrame = 1
    flatsHidden = 2
    rearSurfHidden = 3
# class SurfAttr(Enum):


class DisplayModel:

    def __init__(self, modelData: dd.BodyFaces):
        self.model = modelData
        self.displayMode = DispModes.wireFrame
        self.edgesList1 = self.model.get_unique_edges()
        # TODO initialize surface analize

    def set_display_mode(self, mode: DispModes):
        self.displayMode = mode

    def get_edges(self) -> Sequence[int]:
        """returns list of edges to display"""
        return self.edgesList1

    def get_surfaces(self) -> Sequence[int]:
        """returns list of surfaces to display"""
        ...

    class Surfaces:
        """should define attributes if surface:
        belongs to any sort of special kind (flat or cilinder) and to which face it belongs
        orientation - +Z or -Z
        which simple surface are its neighbours
        """
        def __init__(self):
            #TODO get surfaces data from model
            self.facesNormals = self.__faces_normal_count()
            #TODO form flat surfaces on triangles
            ...

        def __faces_normal_count(self) ->np.array:

            ...



class Edges():

    def __init__(self):
        #TODO find collinear edge to each edge
        ...
