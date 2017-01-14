# -*- coding: utf-8 -*-

import math
import numpy as np

from Idx import

class point2d(object):
    """
    2D point of two floats
    """

    def __init__(self, x = np.float32(0.0), y = np.float32(0.0)):
        """
        Constructor. Build point from x and y

        Parameters
        ----------

        x: float
            point X position
        y: float
            point Y position
        """

        self._x = np.float32( x )
        self._y = np.float32( y )

    @property
    def x(self):
        """
        returns: float
            point X position
        """
        return self._x

    @property
    def y(self):
        """
        returns: float
            point Y position
        """
        return self._y

    def __str__(self):
        """
        returns: string
            default string representation
        """
        return "({0}, {1})".format(self._x, self._y)

    def __repr__(self):
        """
        returns: string
            default representation
        """
        return "{0} {1}".format(self._x, self._y)

    def __setitem__(self, i, value):
        """
        Given the index i, set proper item to value
        """
        if i < 0:
            raise IndexError("point2d::__setitem__: negative index {0}".format(i))
        if i == 0:
            self._x = value
            return
        if i == 1:
            self._y = value
            return

        raise IndexError("point2d::__setitem__: too large index {0}".format(i))

    def __getitem__(self, i):
        """
        Given the index i, returns the proper item
        """
        if i < 0:
            raise IndexError("point2d::__getitem__: negative index {0}".format(i))
        if i == 0:
            return self._x
        if i == 1:
            return self._y

        raise IndexError("point2d::__getitem__: too large index {0}".format(i))

    @staticmethod
    def remove_dupes(pts, tol):
        """
        Given list of points, remove duplicates
        """

        l = len(pts)
        rc = []
        pt_prev = pts[0]
        rc.append(pt_prev)
        for k in range(1, l):
            pt = pts[k]
            if math.fabs(pt_prev.x() - pt.x()) > tol:
                rc.append(pt)

            pt_prev = pt

        return rc

