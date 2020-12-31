from typing import Sequence

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
