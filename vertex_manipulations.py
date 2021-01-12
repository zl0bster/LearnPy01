from typing import Sequence

import numpy as np

X = 0
Y = 1
Z = 2
R = 0
A = 1
E = 2


def envelope_box_count(points):  # np vertex array
    """Finds max and min coords in all axes to count envelope"""
    xmax = np.max(points[:, 0])
    ymax = np.max(points[:, 1])
    zmax = np.max(points[:, 2])
    xmin = np.min(points[:, 0])
    ymin = np.min(points[:, 1])
    zmin = np.min(points[:, 2])
    return xmin, ymin, zmin, xmax, ymax, zmax


def body_center_count(points):  # np vertex array
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


def quadrantXYZ(pnt1: Sequence[float]) -> int:
    """Returns space quadrant number
    1 - X>0 Y>0 Z>0
    ...
    8 - X<0 Y<0 Z<0
    """
    ...
