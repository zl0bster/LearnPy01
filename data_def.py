from typing import Sequence, Optional

import numpy as np

"""Following 3D data types are defined here
    XYZ-point
    DAE-point
    edge
    flat surface
    surface body"""


class PointXYZ():
    # x, y, z: float mm
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def get(self) -> Sequence[float]:
        return self.x, self.y, self.z

    def set(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def toDAE(self) -> Sequence[float]:
        # todo solve zero division exception
        xyDist = self.x ** 2 + self.y ** 2
        d = pow(xyDist + self.z ** 2, 0.5)
        a = np.arctan(self.y / self.x)
        e = np.arctan(self.z / (xyDist ** 0.5))
        return d, a, e

    def toDAErel(self, b: object) -> Sequence[float]:  # b: PointXYZ
        # todo solve zero division exception
        xr, yr, zr = b.get()
        dx = self.x - xr
        dy = self.y - yr
        dz = self.z - zr
        xyDist = dx ** 2 + dy ** 2
        d = pow(xyDist + dz ** 2, 0.5)
        a = np.arctan(dy / dx)
        e = np.arctan(dz / (xyDist ** 0.5))
        return d, a, e

    def __eq__(self, other) -> bool:
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False


class PointDAE():
    # Distance, Azimuth, Elevation: float mm and radians
    def __init__(self, d: float, a: float, e: float):
        self.d = d
        self.a = a
        self.e = e

    def get(self) -> Sequence[float]:
        return self.d, self.a, self.e

    def set(self, d: float, a: float, e: float):
        self.d = d
        self.a = a
        self.e = e

    def toXYZ(self) -> Sequence[float]:
        # todo solve zero division exception
        xyDist = self.d * np.tan(self.e)
        z = self.d / np.tan(self.e)
        x = xyDist * np.cos(self.a)
        y = xyDist * np.sin(self.a)
        return x, y, z

    def __eq__(self, other) -> bool:
        if self.d == other.d and self.a == other.a and self.e == other.e:
            return True
        return False


class PointsList():
    """Keeps the unique points in list. Points cannot be removed.
    Points type is defined while initialization.
    Gives ID for each added Point.
    Points list may be exported to Numpy array.
    """

    LISTTYPE = ['XYZ', 'DAE']

    def __init__(self, listType='XYZ'):  # XYZ or DAE
        self.XYZtype = False
        self.DAEtype = False
        if listType == self.LISTTYPE[0]:
            self.XYZtype = True
        if listType == self.LISTTYPE[1]:
            self.DAEtype = True
        self.points = []

    def add_point(self, pntData: object) -> int:
        # print(type(pntData), pntData) # debug
        if isinstance(pntData, PointXYZ) and not self.XYZtype:
            raise TypeError
        if isinstance(pntData, PointDAE) and not self.DAEtype:
            raise TypeError
        if isinstance(pntData, tuple):
            a, b, c = pntData
        elif isinstance(pntData, list):
            a, b, c = tuple(pntData)
        else:
            a, b, c = pntData.get()
        if len(self.points):
            for i, val in enumerate(self.points):
                if val[0] == a and val[1] == b and val[2] == c:
                    return i
        self.points.append([a, b, c])
        # print(self.points) # debug
        return len(self.points) - 1

    def get_point(self, i: int) -> Sequence[float]:
        if i >= len(self.points):
            raise IndexError
        val = self.points[i]
        return tuple(val)

    def __len__(self):
        return len(self.points)

    def np_array(self):
        return np.asfarray(self.points)


class EdgeList():
    """Keeps the unique edges list. Items cannot be removed.
    Gives ID for each added Edge.
    """

    def __init__(self):
        self.edges = []

    def __len__(self):
        return len(self.edges)

    def add_edge(self, v1: int, v2: int) -> int:
        if len(self.edges):
            for i, val in enumerate(self.edges):
                if val[0] == v1 and val[1] == v2:
                    return i
        self.edges.append([v1, v2])
        return len(self.edges) - 1

    def get_edge(self, i: int) -> Sequence[int]:
        if i >= len(self.edges):
            raise IndexError
        val = self.edges[i]
        return tuple(val)


class Face():
    """Keeps vertex list, edges list. May keep center point and normal vector"""

    def __init__(self, vertexes: Optional[Sequence[int]], edges: Optional[Sequence[int]]):
        self.vertexes = [int]
        self.edges = [int]
        if vertexes:
            self.set_vertexes(vertexes)
        if edges:
            self.set_edges(edges)

    def set_vertexes(self, vxs: Sequence[int]):
        if isinstance(vxs, list):
            a, b, c = tuple(vxs)
        else:
            a, b, c = vxs
        self.vertexes = [a, b, c]

    def set_edges(self, eds: Sequence[int]):
        if isinstance(eds, list):
            a, b, c = tuple(eds)
        else:
            a, b, c = eds
        self.edges = [a, b, c]

    def get_vertexes(self):
        return tuple(self.vertexes)

    def get_edges(self):
        return tuple(self.edges)


class FaceList():
    """Keeps the unique Faces list. Items cannot be removed.
    Gives ID for each added Face."""

    def __init__(self):
        self.faces = []

    def __len__(self):
        return len(self.faces)

    def add_face(self, face: Face) -> int:
        if len(self.faces):
            for i, val in enumerate(self.faces):
                if val == face:
                    return i
        self.faces.append(face)
        return len(self.faces) - 1

    def get_face(self, i: int) -> tuple:
        if i >= len(self.faces):
            raise IndexError
        return self.faces[i]


class BodyFaces():
    """Keeps center coords, orientation.
    Contains VartexList, EdgesList, FacesList

    """

    def __init__(self):
        self.centerXYZ = PointXYZ(0, 0, 0)
        self.normalDAE = PointDAE(1, 0, 0)
        self.vertexes = PointsList(listType="XYZ")
        self.edges = EdgeList()
        self.faces = FaceList()

    def add_face(self, facePoints: Sequence[Sequence[float]]):
        vertexes = []
        edges = []
        for point in facePoints:
            vertexes.append(self.vertexes.add_point(point))
        for i, vx in enumerate(vertexes):
            a = vx
            if i == len(vertexes) - 1:
                b = vertexes[0]
            else:
                b = vertexes[i + 1]
            edges.append(self.edges.add_edge(a, b))
        if len(vertexes) > 3:
            raise OverflowError
        currFace = Face(vertexes=vertexes, edges=edges)
        self.faces.add_face(currFace)

    def __len__(self):
        return len(self.faces)

    # def __iter__(self):
    #     self.nIterFace = 0
    #     return self
    #
    # def __next__(self):
    #     if self.nIterFace == len(self.faces):
    #         raise StopIteration
    #     self.nIterFace += 1
    #     return self.faces.get_face(self.nIterFace)

    def get_vxs_np_array(self):
        return self.vertexes.np_array()

    def get_centerXYZ(self) -> Sequence[float]:
        return self.centerXYZ.get()

    def set_centerXYZ(self, pointXYZ: Sequence[float]):
        if isinstance(pointXYZ, tuple):
            self.centerXYZ.set(pointXYZ)
        elif isinstance(pointXYZ, list):
            self.centerXYZ.set(tuple(pointXYZ))
        else:
            raise TypeError

    def get_normal(self) -> Sequence[float]:
        return self.normalDAE.get()

    def set_normal(self, pointDAE: Sequence[float]):
        if isinstance(pointDAE, tuple):
            self.normalDAE.set(pointDAE)
        elif isinstance(pointDAE, list):
            self.normalDAE.set(tuple(pointDAE))
        else:
            raise TypeError

    def get_all_edges(self):
        edgeList = []
        for i in range(len(self.edges)):
            edgeList.append(self.edges.get_edge(i))
        return edgeList

    def get_edges_list(self):
        faceList = []
        for i in range(len(self.faces)):
            face = self.faces.get_face(i)
            faceEdges = face.get_edges()
            faceList.append(faceEdges)
        return faceList

    def get_vertex_list(self):
        faceList = []
        for i in range(len(self.faces)):
            face = self.faces.get_face(i)
            faceVXs = face.get_vertexes()
            faceList.append(faceVXs)
        return faceList

    def get_face_vertexes(self, i: int) -> Sequence[int]:
        if i >= len(self.faces):
            raise IndexError
        face = self.faces.get_face(i)
        return face.get_vertexes()

    def get_face_edges(self, i: int) -> Sequence[int]:
        if i >= len(self.faces):
            raise IndexError
        face = self.faces.get_face(i)
        return face.get_edges()
