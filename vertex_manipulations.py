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
    # arShape = [pts.shape[0], 4]
    arShape = pts.shape
    result = np.zeros(arShape)
    for i in range(pts.shape[0]):
        if pts[i].any() == 0:
            continue
        # currentPt = pts[i].tolist()
        # q = quadrantXYZ(currentPt)
        result[i, R] = np.sqrt(np.power(pts[i, X], 2) + np.power(pts[i, Y], 2) + np.power(pts[i, Z], 2))
        result[i, E] = np.arcsin(pts[i, Z] / result[i, R])
        lenXY = np.hypot(pts[i, X], pts[i, Y])
        if not lenXY == 0:
            if pts[i, X] < 0:
                result[i, A] = np.pi - np.arcsin(pts[i, Y] / lenXY)
            else:
                result[i, A] = np.arcsin(pts[i, Y] / lenXY)
        # result[i, Q] = q
    return result


def arrayDAEtoXYZ(pts):  # np vertex array in DAE
    """Transforms angular coordinates array to decart"""
    # arShape = [pts.shape[0], 3]
    arShape = pts.shape
    result = np.zeros(arShape)
    for i in range(pts.shape[0]):
        if pts[i].any() == 0:
            continue
        result[i, X] = pts[i, R] * np.cos(pts[i, E]) * np.cos(pts[i, A])
        result[i, Y] = pts[i, R] * np.cos(pts[i, E]) * np.sin(pts[i, A])
        result[i, Z] = pts[i, R] * np.sin(pts[i, E])
        if np.abs(result[i, X]) < 1.0e-12:
            result[i, X] = 0
        if np.abs(result[i, Y]) < 1.0e-12:
            result[i, Y] = 0
    return result


def shift2pi_correction(angle: float) -> float:
    result = angle
    if angle > np.pi:
        result = -2 * np.pi + angle
    if angle < -np.pi:
        result = 2 * np.pi + angle
    return result


def arrayDAEturn(pts, a: float, e: float):
    result = np.zeros(pts.shape)
    for i in range(pts.shape[0]):
        result[i, R] = pts[i, R]
        result[i, A] = pts[i, A] + a
        result[i, E] = pts[i, E]  # + e
        result[i, A] = shift2pi_correction(result[i, A])
        result[i, E] = shift2pi_correction(result[i, E])
    return result


def arrayXYZrotX(pts, a: float):
    result = np.zeros(pts.shape)
    cosA = np.cos(a)
    sinA = np.sin(a)
    for i in range(pts.shape[0]):
        result[i, X] = pts[i, X]
        result[i, Y] = pts[i, Y] * cosA + pts[i, Z] * (-sinA)
        result[i, Z] = pts[i, Y] * sinA + pts[i, Z] * cosA
    return result


def arrayXYZrotY(pts, a: float):
    result = np.zeros(pts.shape)
    cosA = np.cos(a)
    sinA = np.sin(a)
    for i in range(pts.shape[0]):
        result[i, Y] = pts[i, Y]
        result[i, X] = pts[i, X] * cosA + pts[i, Z] * sinA
        result[i, Z] = pts[i, X] * (-sinA) + pts[i, Z] * cosA
    return result


def arrayXYZrotZ(pts, a: float):
    result = np.zeros(pts.shape)
    cosA = np.cos(a)
    sinA = np.sin(a)
    for i in range(pts.shape[0]):
        result[i, Z] = pts[i, Z]
        result[i, X] = pts[i, X] * cosA + pts[i, Y] * (-sinA)
        result[i, Y] = pts[i, X] * sinA + pts[i, Y] * cosA
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
