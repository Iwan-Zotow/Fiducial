# -*- coding: utf-8 -*-

from __future__ import print_function

import OCC.TopoDS
import aocutils.display.topology

r"""This module several helper functions to deal with CAD STEP data"""

def get_surface(surface):
    """
    Given surface or its handle, return what kind it is
    """
    surfaces = ["Geom_BezierSurface", "Geom_BSplineSurface", "Geom_RectangularTrimmedSurface",
                "Geom_ConicalSurface", "Geom_CylindricalSurface", "Geom_Plane", "Geom_SphericalSurface",
                "Geom_ToroidalSurface", "Geom_SurfaceOfLinearExtrusion", "Geom_SurfaceOfRevolution"]
    ss = surface
    if "Handle" in str(type(ss)): # we got handle, getting actual surface
        ss = surface.GetObject()

    for s in surfaces:
        if ss.IsKind(s):
            return s

    return None

def get_curve(curve):
    """
    Given curve or its handle, return what kind it is
    """
    curves = ["Geom_BezierCurve", "Geom_BSplineCurve", "Geom_TrimmedCurve",
              "Geom_Circle", "Geom_Ellipse", "Geom_Hyperbola", "Geom_Parabola"]

    cc = curve
    if "Handle" in str(type(cc)): # we got handle, getting actual surface
        cc = curve.GetObject()

    for c in curves:
        if cc.IsKind(c):
            return c

    return None

def str_shape(sh_type):
    """
    Given the shape type, returns shape description
    """
    types = ["COMPOUND", "COMPSOLID", "SOLID", "SHELL", "FACE", "WIRE", "EDGE", "VERTEX"]
    return types[sh_type]

def factory_shapes(shape):
    """
    upgrade shape based on type
    NB: aocutils.topology.shape_to_topology(shape) plays the same role
    """
    t = shape.ShapeType()

    if (t == OCC.TopAbs.TopAbs_COMPOUND):
        return OCC.TopoDS.topods.Compound(shape)

    if (t == OCC.TopAbs.TopAbs_COMPSOLID):
        return OCC.TopoDS.topods.CompSolid(shape)

    if (t == OCC.TopAbs.TopAbs_SOLID):
        return OCC.TopoDS.topods.Solid(shape)

    if (t == OCC.TopAbs.TopAbs_SHELL):
        return OCC.TopoDS.topods.Shell(shape)

    if (t == OCC.TopAbs.TopAbs_FACE):
        return OCC.TopoDS.topods.Face(shape)

    if (t == OCC.TopAbs.TopAbs_WIRE):
        return OCC.TopoDS.topods.Wire(shape)

    if (t == OCC.TopAbs.TopAbs_EDGE):
        return OCC.TopoDS.topods.Edge(shape)

    if (t == OCC.TopAbs.TopAbs_VERTEX):
        return OCC.TopoDS.topods.Vertex(shape)

    return None

def print_solids(shape):
    """
    print solids of the shape
    """
    the_solids = aocutils.topology.Topo(shape, return_iter=False).solids
    for i, solid in enumerate(the_solids):
        print("{0} {1}".format(i, type(solid)))

def print_shells(shape):
    """
    print shells of the shape
    """
    the_shells = aocutils.topology.Topo(shape, return_iter=False).shells
    for i, shell in enumerate(the_shells):
        print("{0} {1}".format(i, type(shell)))

def print_faces(shape):
    """
    print faces of the shape
    """
    the_faces = aocutils.topology.Topo(shape, return_iter=False).faces
    for i, face in enumerate(the_faces):
        print("{0} {1}".format(i, type(face)))

def print_edges(shape):
    """
    print edges of the shape
    """
    the_edges = aocutils.topology.Topo(shape, return_iter=False).edges
    for i, edge in enumerate(the_edges):
        print("{0} {1}".format(i, type(edge)))

def print_wires(shape):
    """
    print wires of the shape
    """
    the_wires = aocutils.topology.Topo(shape, return_iter=False).wires
    for i, wire in enumerate(the_wires):
        print("{0} {1}".format(i, type(wire)))

def print_all(shape, separator = None):
    """
    Print all pieces of the shape, with optional separator in between
    """
    print_solids(shape)
    if separator != None:
        print(separator)
    print_shells(shape)
    if separator != None:
        print(separator)
    print_faces(shape)
    if separator != None:
        print(separator)
    print_edges(shape)
    if separator != None:
        print(separator)
    print_wires(shape)
