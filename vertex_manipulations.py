from typing import Sequence

import numpy as np

X = 0
Y = 1
Z = 2
R = 0
A = 1
E = 2
Q = 3


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
    arShape = [pts.shape[0], 4]
    result = np.zeros(arShape)
    for i in range(pts.shape[0]):
        if pts[i].any() == 0:
            continue
        currentPt = pts[i].tolist()
        aCorrection = 0
        q = quadrantXYZ(currentPt)
        if q == 6 or q == 8:
            aCorrection = -np.pi / 2
        elif q == 2 or q == 4:
            aCorrection = np.pi / 2
        result[i, R] = np.sqrt(np.power(pts[i, X], 2) + np.power(pts[i, Y], 2) + np.power(pts[i, Z], 2))
        result[i, E] = np.arcsin(pts[i, Z] / result[i, R])
        lenXY = np.hypot(pts[i, X], pts[i, Y])
        if not lenXY == 0:
            result[i, A] = np.arcsin(pts[i, Y] / lenXY) + aCorrection
        result[i, Q] = q
    return result


def arrayDAEtoXYZ(pts):  # np vertex array in DAE
    """Transforms angular coordinates array to decart"""
    arShape = [pts.shape[0], 3]
    result = np.zeros(arShape)
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


def arrayDAEtoDEG(pts):  # np vertex array in DAE
    """Transforms angular values from radians to degrees"""
    result = np.zeros(pts.shape)
    for i in range(pts.shape[0]):
        result[i, R] = pts[i, R]
        result[i, A] = np.degrees(pts[i, A])
        result[i, E] = np.degrees(pts[i, E])
    return result


def quadrantXYZ(pnt1: Sequence[float]) -> int:
    """Returns space quadrant number
    0 - X=0 Y=0 Z<>0
    1 - X>0 Y>0 Z>0
    ...
    8 - X<0 Y<0 Z<0
    """
    x = pnt1[X]
    y = pnt1[Y]
    z = pnt1[Z]
    if x == 0 and y == 0:
        return 0
    q = 1 + (x < 0) + 2 * (y < 0) + 4 * (z < 0)
    return q


def quadrantDAE(pnt1: Sequence[float]) -> int:
    """Returns space quadrant number
    0 - X=0 Y=0 Z<>0    A - NaN E = pi/2|1.5*pi
    1 - X>0 Y>0 Z>0
    ...
    8 - X<0 Y<0 Z<0
    """
    r = pnt1[R]
    a = pnt1[A]
    e = pnt1[E]
