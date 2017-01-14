# coding: utf-8

from point2d import point2d
from point3d import point3d

def write2d(f, points):
    """
    Given the list of 2D points, write them to file f
    """

    if len(points) == 0:
        return

    f.write("{0}\n".format(len(points)))

    for pt in points:
        f.write("{0}\n".format(repr(pt)))

def write3dcon(f, l):
    """
    Given length l write connectivity string to f
    """

    if l <= 1: # at least 2
        return

    f.write("{0}\n".format(l-1))
    for k in range(0, l-1):
        f.write("{0} {1}\n".format(k, k+1))

def write3d(f, points):
    """
    Given the list of 3D points, write them to file f
    """

    l = len(points)
    if l == 1:
        return

    f.write("{0}\n".format(l))

    for pt in points:
        f.write("{0}\n".format(repr(pt)))
    write3dcon(f, l)

if __name__ == "__main__":

    pts2d = list()
    pts2d.append(point2d(1.0, 2.0))
    pts2d.append(point2d(2.0, 1.0))

    pts3d = list()
    pts3d.append(point3d(1.0, 2.0, 3.0))
    pts3d.append(point3d(1.0, 3.0, 2.0))
    pts3d.append(point3d(5.0, 2.0, 3.0))

    fname = "aaa.ocp"
    with open(fname, 'w+') as f:
        write2d(f, pts2d)
        write3d(f, pts3d)
