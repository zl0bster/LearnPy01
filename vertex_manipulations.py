""" Module contains math 3D operations with vertex numpy array

"""

from typing import Sequence

import numpy as np
from loguru import logger

X = 0
Y = 1
Z = 2
R = 0
A = 1
E = 2
Q = 3

DEBUG = 1
GAP: np.float32 = 0.005


def envelope_box_count(points: np.array) -> Sequence[float]:  # np vertex array
    """Finds max and min coords in all axes to count envelope box"""
    xmax = np.max(points[:, 0])
    ymax = np.max(points[:, 1])
    zmax = np.max(points[:, 2])
    xmin = np.min(points[:, 0])
    ymin = np.min(points[:, 1])
    zmin = np.min(points[:, 2])
    return xmin, ymin, zmin, xmax, ymax, zmax


def body_center_count(points: np.array) -> Sequence[float]:  # np vertex array
    """Counts center coord of envelope"""
    xmin, ymin, zmin, xmax, ymax, zmax = envelope_box_count(points)
    xmin = abs(xmin) if xmin < 0 else -xmin
    ymin = abs(ymin) if ymin < 0 else -ymin
    zmin = abs(zmin) if zmin < 0 else -zmin
    x = (xmax + xmin) / 2
    y = (ymax + ymin) / 2
    z = (zmax + zmin) / 2
    return x, y, z


def arrayXYZtoDAE(pts: np.array) -> np.array:  # np vertex array in XYZ
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


def arrayDAEtoXYZ(pts: np.array) -> np.array:  # np vertex array in DAE
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
    '''corrects angle in radians when it is more than 180 degrees'''
    result = angle
    if angle > np.pi:
        result = -2 * np.pi + angle
    if angle < -np.pi:
        result = 2 * np.pi + angle
    return result


def arrayDAEturn(pts: np.array, a: float, e: float) -> np.array:
    '''Turn all array points in spherical implemention'''
    result = np.zeros(pts.shape)
    for i in range(pts.shape[0]):
        result[i, R] = pts[i, R]
        result[i, A] = pts[i, A] + a
        result[i, E] = pts[i, E]  # + e
        result[i, A] = shift2pi_correction(result[i, A])
        result[i, E] = shift2pi_correction(result[i, E])
    return result


def arrayXYZrotX(pts: np.array, a: float) -> np.array:
    ''' Turn all points od pts-array around X axis for a-radians'''
    result = np.zeros(pts.shape)
    cosA = np.cos(a)
    sinA = np.sin(a)
    for i in range(pts.shape[0]):
        result[i, X] = pts[i, X]
        result[i, Y] = pts[i, Y] * cosA + pts[i, Z] * (-sinA)
        result[i, Z] = pts[i, Y] * sinA + pts[i, Z] * cosA
    return result


def arrayXYZrotY(pts: np.array, a: float) -> np.array:
    ''' Turn all points od pts-array around Y axis for a-radians'''
    result = np.zeros(pts.shape)
    cosA = np.cos(a)
    sinA = np.sin(a)
    for i in range(pts.shape[0]):
        result[i, Y] = pts[i, Y]
        result[i, X] = pts[i, X] * cosA + pts[i, Z] * sinA
        result[i, Z] = pts[i, X] * (-sinA) + pts[i, Z] * cosA
    return result


def arrayXYZrotZ(pts: np.array, a: float) -> np.array:
    ''' Turn all points od pts-array around Z axis for a-radians'''
    result = np.zeros(pts.shape)
    cosA = np.cos(a)
    sinA = np.sin(a)
    for i in range(pts.shape[0]):
        result[i, Z] = pts[i, Z]
        result[i, X] = pts[i, X] * cosA + pts[i, Y] * (-sinA)
        result[i, Y] = pts[i, X] * sinA + pts[i, Y] * cosA
    return result


def pointsXYZdelta(pnt1: Sequence[float], pnt2: Sequence[float]) -> Sequence[float]:
    '''Counts relative distance between points '''
    x = pnt2[X] - pnt1[X]
    y = pnt2[Y] - pnt1[Y]
    z = pnt2[Z] - pnt1[Z]
    return x, y, z


def array_plus_point(pts: np.array, pt: Sequence[float]) -> np.array:  # np vertex array in XYZ or DAE
    """ADDs point's XYZ to each line of array
    to shift body center """
    result = np.zeros(pts.shape)
    for i in range(pts.shape[0]):
        result[i, X] = pts[i, X] + pt[X]
        result[i, Y] = pts[i, Y] + pt[Y]
        result[i, Z] = pts[i, Z] + pt[Z]
    return result


def arrayDAEtoDEG(pts: np.array) -> np.array:  # np vertex array in DAE
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


def make_surf_MX_from_VX_array(vxs: np.array, pts: Sequence[int]) -> np.array:
    """creates surface matrix for normal count"""
    result = []
    # print("make surface from these points",vxs)
    for ind in pts:
        # print(ind, '-', vxs[ind])
        logger.debug(f'vertex {ind} - {vxs[ind]}')
        result.append(list(vxs[ind]))
    return np.array(result)


def count_norm_to_surf(vxs: np.array) -> Sequence[float]:
    """creates minor matrixes and counts their determinants
    to define vector normal to surface
    vxs - [ x, y, z] of 3 vertexes"""
    result = np.zeros(3)
    minorIndxs = [[1, 2, 1], [0, 2, -1], [0, 1, 1]]
    for i in range(3):
        # coordIsSame = np.equal(vxs[0, i],  vxs[1, i]) and np.equal(vxs[1, i], vxs[2, i])
        coordIsSame = (np.abs(vxs[0, i] - vxs[1, i]) < GAP) and (np.abs(vxs[1, i] - vxs[2, i]) < GAP)
        if coordIsSame:
            result[minorIndxs[i][0]] = 0.
            result[minorIndxs[i][1]] = 0.
            result[i] = 1.
    if np.max(result) == 0:
        for i in range(3):
            minor = np.zeros([2, 2])
            minor[0, 0] = vxs[1, minorIndxs[i][0]]
            minor[0, 1] = vxs[1, minorIndxs[i][1]]
            minor[1, 0] = vxs[2, minorIndxs[i][0]]
            minor[1, 1] = vxs[2, minorIndxs[i][1]]
            minorVal = np.round(minorIndxs[i][2] * np.linalg.det(minor))
            # minorVal = minorIndxs[i][2] * (minor[0, 0] * minor[1, 1] - minor[1, 0] * minor[0, 1])
            val = vxs[i, 0] * minorVal
            result[i] = val
        maxVal = np.max(np.abs(result))
        result = result / maxVal
    logger.debug(f'count_normal\n{vxs}')
    logger.debug(f'normalized vectors \n {result}')
    # if DEBUG:
    #     print('* ' * 10)
    #     print(vxs)
    #     # print('max value:', maxVal)
    #     print('normalized:', result)
    return result

logger.add('vert_manip.log')
logger.level("ERROR")