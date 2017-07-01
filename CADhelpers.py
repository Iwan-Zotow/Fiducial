# -*- coding: utf-8 -*-
import sys

from typing import List

import OCC.TopoDS
import aocutils.display.topology

from XcMath        import utils

from point3d       import point3d
from point2d       import point2d

# http://opencascade.blogspot.com/2009/02/topology-and-geometry-in-open-cascade_12.html

r"""This module contains several helper functions to deal with CAD STEP data"""

surfaces: List[str] = ["Geom_BezierSurface", "Geom_BSplineSurface", "Geom_RectangularTrimmedSurface",
                       "Geom_ConicalSurface", "Geom_CylindricalSurface", "Geom_Plane", "Geom_SphericalSurface",
                       "Geom_ToroidalSurface", "Geom_SurfaceOfLinearExtrusion", "Geom_SurfaceOfRevolution"]

curves: List[str] = ["Geom_BezierCurve", "Geom_BSplineCurve", "Geom_TrimmedCurve",
                     "Geom_Circle", "Geom_Ellipse", "Geom_Hyperbola", "Geom_Parabola",
                     "Geom_Line", "Geom_OffsetCurve", "ShapeExtend_ComplexCurve"]


def get_surface(surface) -> str:
    """
    Given surface or its handle, return what kind it is
    """
    ss = surface
    if "Handle" in str(type(ss)): # we got handle, getting actual surface
        ss = surface.GetObject()

    for s in surfaces:
        if ss.IsKind(s):
            return s

    return None


def get_curve(curve) -> str:
    """
    Given curve or its handle, return what kind it is
    """
    cc = curve
    if "Handle" in str(type(cc)): # we got handle, getting actual surface
        cc = curve.GetObject()

    for c in curves:
        if cc.IsKind(c):
            return c

    return None


def str_shape(sh_type: int) -> str:
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


def cast_surface(surface):
    """
    Given the base surface handle, cast it to the actual one
    """
    if not ("Handle" in str(type(surface))): # it is not a handle, bail out
        return None

    ss: str = get_surface(surface)
    if ss is None:
        return None

    if ss == "Geom_BezierSurface":
        return OCC.Geom.Handle_Geom_BezierSurface.DownCast(surface)
    if ss == "Geom_BSplineSurface":
        return OCC.Geom.Handle_Geom_BSplineSurface.DownCast(surface)
    if ss == "Geom_RectangularTrimmedSurface":
        return OCC.Geom.Handle_Geom_RectangularTrimmedSurface.DownCast(surface)
    if ss == "Geom_ConicalSurface":
        return OCC.Geom.Handle_Geom_ConicalSurface.DownCast(surface)
    if ss == "Geom_Plane":
        return OCC.Geom.Handle_Geom_Plane.DownCast(surface)
    if ss == "Geom_SphericalSurface":
        return OCC.Geom.Handle_Geom_SphericalSurface.DownCast(surface)
    if ss == "Geom_ToroidalSurface":
        return OCC.Geom.Handle_Geom_ToroidalSurface.DownCast(surface)
    if ss == "Geom_SurfaceOfLinearExtrusion":
        return OCC.Geom.Handle_Geom_SurfaceOfLinearExtrusion.DownCast(surface)
    if ss == "Geom_SurfaceOfRevolution":
        return OCC.Geom.Handle_Geom_SurfaceOfRevolution.DownCast(surface)

    return None


def cast_curve(curve):
    """
    Given the base curve handle, cast it to the actual one
    """
    if not ("Handle" in str(type(curve))): # it is not a handle, bail out
        return None

    cc = get_curve(curve)
    if cc is None:
        return None

    if cc == "Geom_BezierCurve":
        return OCC.Geom.Handle_Geom_BezierCurve.DownCast(curve)
    if cc == "Geom_BSplineCurve":
        return OCC.Geom.Handle_Geom_BSplineCurve.DownCast(curve)
    if cc == "Geom_TrimmedCurve":
        return OCC.Geom.Handle_Geom_TrimmedCurve.DownCast(curve)
    if cc == "Geom_Circle":
        return OCC.Geom.Handle_Geom_Circle.DownCast(curve)
    if cc == "Geom_Ellipse":
        return OCC.Geom.Handle_Geom_Ellipse.DownCast(curve)
    if cc == "Geom_Hyperbola":
        return OCC.Geom.Handle_Geom_Hyperbola.DownCast(curve)
    if cc == "Geom_Parabola":
        return OCC.Geom.Handle_Geom_Parabola.DownCast(curve)
    if cc == "Geom_Line":
        return OCC.Geom.Handle_Geom_Line.DownCast(curve)
    if cc == "Geom_OffsetCurve":
        return OCC.Geom.Handle_Geom_OffsetCurve.DownCast(curve)
    if cc == "ShapeExtend_ComplexCurve":
        return OCC.Geom.Handle_ShapeExtend_ComplexCurve.DownCast(curve)

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

def surface2gnuplot(surface, Nu:int = 40, Nv:int = 40) -> List[List[point3d]]:
    """
    Makes gnuplot representation of a surface,
    returns both spatial values and parameters
    """
    U1, U2, V1, V2 = surface.Bounds()

    if U1 > 2e99 or U1 < -2e99:
        return None

    if U2 > 2e99 or U2 < -2e99:
        return None

    if V1 > 2e99 or V1 < -2e99:
        return None

    if V2 > 2e99 or V2 < -2e99:
        return None

    stepu = (U2 - U1) / float(Nu)
    stepv = (V2 - V1) / float(Nv)

    pt = OCC.gp.gp_Pnt()
    blocks = list()
    for ku in range(0, Nu+1):
        u = utils.clamp(U1 + float(ku)*stepu, U1, U2)
        block = list()
        for kv in range(0, Nv+1):
            v = utils.clamp(V1 + float(kv)*stepv, V1, V2)
            surface.D0(u, v, pt)
            block.append((point3d(pt.X(), pt.Z(), pt.Y()), point2d(u, v)))
        blocks.append(block)

    return blocks


def save_gnuplot_surface(prefix: str, i:int, blocks, full: bool = False):
    """
    Save sphere block in the gnuplot format,
    if full is set, print parameters as well
    """
    if blocks is None:
        return

    fname: str = prefix + "_" + str(i) + ".dat"
    with open(fname, "w", encoding="utf-8") as f:
        for block in blocks:
            for pt in block:
                pt3, pt2 = pt
                if full:
                    s = "  {0}    {1}    {2}    {3}    {4}\n".format(pt3.x, pt3.y, pt3.z, pt2.x, pt2.y)
                else:
                    s = "  {0}    {1}    {2}\n".format(pt3.x, pt3.y, pt3.z)
                f.write(s)
            f.write("\n")


def write_ICP(RU, OuterCup, InnerCup, shift, yiw, riw, yow, row):
    """
    write the ICP compatible data to file
    """
    fname = "R" + str(RU) + "O" + str(OuterCup) + "I" + InnerCup + ".icp"

    with open(fname, 'w') as os:
        save_ICP(RU, OuterCup, InnerCup, shift, yiw, riw, yow, row, os)


def save_ICP(RU, OuterCup, InnerCup, shift, yiw, riw, yow, row, os = sys.stdout):
    """
    write the ICP compatible data to output stream os
    """
    if RU is None:
        return

    if yiw is None:
        return

    if riw is None:
        return

    if yow is None:
        return

    if row is None:
        return

    # RU
    os.write(RU)
    os.write("\n")

    # Outer cup
    os.write(OuterCup)
    os.write("\n")

    # Inner cup
    os.write(InnerCup)
    os.write("\n")

    # nof points in the inner wall
    niw = len(riw)
    if niw != len(yiw):
        return None
    os.write(str(niw))
    os.write("\n")

    # inner wall
    for r, y in zip(riw, yiw):
        os.write("{0:13.6e} {1:13.6e}\n".format(shift - y, r))

    # nof points in the outer wall
    now = len(row)
    if now != len(yow):
        return None
    os.write(str(now))
    os.write("\n")

    # outer wall
    for r, y in zip(row, yow):
        os.write("{0:13.6e} {1:13.6e}\n".format(shift - y, r))


def print_flags(shape):
    """
    print flags for a shape
    """
    t = OCC.BRepCheck.BRepCheck_Analyzer(shape)
    print(t.IsValid())
    print(shape.Checked())
    print(shape.Closed())
    print(shape.Convex())
    print(shape.Free())
    print(shape.Infinite())
