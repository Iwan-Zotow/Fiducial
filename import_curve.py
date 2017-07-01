# coding: utf-8

from __future__ import print_function

import sys
import math
import numpy as np
import logging

from functools import partial

import OCC.TopoDS
import OCC.Display.SimpleGui

import aocutils.display.topology
import aocutils.display.backends

import aocxchange.step
import aocxchange.utils

import CADhelpers
import DISPhelpers

from XcMath          import utils
from XcIO.write_OCP  import write_OCP

from rdp             import rdp

from point2d import point2d
from point3d import point3d

def display_all(display, shape):
    """
    display every part of the shape
    """
    add_menu('solids')
    dsolids = partial(DISPhelpers.display_solids, display, shape)
    dsolids.__name__ = "dsolids"
    add_function_to_menu('solids', dsolids)
    add_menu('edges')
    dedges = partial(DISPhelpers.display_edges, display, shape)
    dedges.__name__ = "dedges"
    add_function_to_menu('edges', dedges)
    add_menu('faces')
    dfaces = partial(DISPhelpers.display_faces, display, shape)
    dfaces.__name__ = "dfaces"
    add_function_to_menu('faces', dfaces)
    add_menu('shells')
    dshells = partial(DISPhelpers.display_shells, display, shape)
    dshells.__name__ = "dshells"
    add_function_to_menu('shells', dshells)
    add_menu('wires')
    dwires = partial(DISPhelpers.display_wires, display, shape)
    dwires.__name__ = "dwires"
    add_function_to_menu('wires', dwires)

def readSTEP(filename):
    """
    Given the STEP filename, read shapes from it
    """
    fname = aocxchange.utils.path_from_file(__file__, filename)
    importer = aocxchange.step.StepImporter(fname)

    return importer.shapes

def print_shapes():
    """
    print default shapes in ascending order, from
    https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_topo_d_s___shape.html
    """
    print("----------------------------")
    print(OCC.TopAbs.TopAbs_COMPOUND)
    print(OCC.TopAbs.TopAbs_COMPSOLID)
    print(OCC.TopAbs.TopAbs_SOLID)
    print(OCC.TopAbs.TopAbs_SHELL)
    print(OCC.TopAbs.TopAbs_FACE)
    print(OCC.TopAbs.TopAbs_WIRE)
    print(OCC.TopAbs.TopAbs_EDGE)
    print(OCC.TopAbs.TopAbs_VERTEX)
    print("----------------------------")

def main(filename):
    """
    process single fiducial from filename
    """
    shapes = readSTEP(filename)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Number of shapes: {0}".format(len(shapes)))
    for shape in shapes:
        print("{0}: {1}".format(shape.ShapeType(), CADhelpers.str_shape(shape.ShapeType())))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    shape = shapes[0]
    print(type(shape))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    sol = aocutils.topology.shape_to_topology(shape) # sol = factory_shapes(shape)

    print(type(sol))

    return sol

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

def compute_bspline_midline(bspline, Nv = 100, Nu = 1024):
    """
    Given the bspline surface with one open and one closed/periodic parameter,
    compute middle/center line assuming closed parameter is a circle

    Nu - number of points in U space, how much points will be returned
    Nv - number of points in V space, how much to use to compute middle point

    Returns array of 3d points for curve, array of 2d points for cup outline
    """
    if bspline is None:
        return None

    if "Geom_BSplineSurface" not in str(type(bspline)):
        return None

    if not bspline.IsUClosed():
        return None

    if not bspline.IsUPeriodic():
        return None

    U1, U2, V1, V2 = bspline.Bounds()

    r2 = list()
    r3 = list()

    pt = OCC.gp.gp_Pnt()

    vstep = (V2 - V1) / float(Nv)
    ustep = (U2 - U1) / float(Nu)
    uwght = 1.0 / float(Nu)

    for kv in range(0, Nv+1):
        v = utils.clamp(V1 + vstep * float(kv), V1, V2)
        x = 0.0
        y = 0.0
        z = 0.0
        rmin = 1000000000.0
        ymin = 0.0
        for ku in range(0, Nu+1):
            u = utils.clamp(U1 + ustep * float(ku), U1, U2)
            ss.D0(u, v, pt)
            x += pt.X()
            y += pt.Y()
            z += pt.Z()
            r = utils.squared(pt.X()) + utils.squared(pt.Z())
            if r < rmin:
                rmin = r
                ymin = pt.Y()

        r2.append(point2d(ymin, math.sqrt(rmin)))
        r3.append(point3d(uwght*x, uwght*y, uwght*z))

    if len(r3) == 0:
        return None

    return (r3, r2)

def convert_fiducial(pts, origin):
    """
    Convert fiducial curve from list of points into proper OCP format
    """
    xfc = list()
    yfc = list()
    zfc = list()

    for pt in pts:
        xfc.append(-pt.z)
        yfc.append(pt.x)
        zfc.append( - (pt.y - origin))

    # first point insertion
    l = math.sqrt(utils.squared(xfc[0] - xfc[1]) + utils.squared(yfc[0] - yfc[1]) + utils.squared(zfc[0] - zfc[1]))
    wx = (xfc[1] - xfc[0]) / l
    wy = (yfc[1] - yfc[0]) / l
    wz = (zfc[1] - zfc[0]) / l

    s = (origin - zfc[0]) / wz

    xfc.insert(0, xfc[0] + wx*s)
    yfc.insert(0, yfc[0] + wy*s)
    zfc.insert(0, zfc[0] + wz*s)

    # last point insertion
    l = math.sqrt(utils.squared(xfc[-1] - xfc[-2]) + utils.squared(yfc[-1] - yfc[-2]) + utils.squared(zfc[-1] - zfc[-2]))
    wx = (xfc[-1] - xfc[-2]) / l
    wy = (yfc[-1] - yfc[-2]) / l
    wz = (zfc[-1] - zfc[-2]) / l

    s = (origin - zfc[-1]) / wz

    xfc.append(xfc[-1] + wx*s)
    yfc.append(yfc[-1] + wy*s)
    zfc.append(zfc[-1] + wz*s)

    return (xfc, yfc, zfc)

def convert_outline(pts, origin):
    """
    Convert 2d points fiducial curve from list of points into proper OCP format
    """
    xow = list()
    yow = list()
    xiw = list()
    yiw = list()

    thickness = 2.0

    rprev = 111111.0
    for pt in pts:
        y = pt.x
        r = pt.y
        if r > rprev:
            break
        l  = math.sqrt(y*y + r*r)
        wr = r / l
        wy = y / l
        xow.append(y)
        yow.append(r)
        xiw.append(y - wy*thickness)
        yiw.append(r - wr*thickness)
        rprev = r

    xow.append(origin - 2.0)
    yow.append(0.0)

    xiw.append(origin - 2.0 + thickness)
    yiw.append(0.0)

    # revert outer and place relative to origin
    xxow = list()
    yyow = list()
    for y, r in zip(xow, yow):
        xxow.insert(0, origin - y)
        yyow.insert(0, r)
    del yow
    del xow

    t = xxow[-1]
    xxow.append(t)
    yyow.append(8.138100e+01)
    xxow.append(-99.0)
    yyow.append(8.600000e+01)
    xxow.append(-99.0)
    yyow.append(8.800000e+01)
    xxow.append(origin)
    yyow.append(8.800000e+01)

    # revert inner and place relative to origin
    xxiw = list()
    yyiw = list()
    for y, r in zip(xiw, yiw):
        xxiw.insert(0, origin - y)
        yyiw.insert(0, r)
    del yiw
    del xiw

    return xxow, yyow, xxiw, yyiw

if __name__ == "__main__":

    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

    sep = "          -----------------             "
    sol = main("cups/XMSGP030A10.01-003 breast_cup_outer_S fiducial wire full.STEP") # "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP"

    backend = aocutils.display.defaults.backend
    display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)
    display_all(display, sol)
    start_display()

    #print_flags(sol)

    #print(sep)
    #CADhelpers.print_all(sol, sep)
    #print(sep)

    the_faces = aocutils.topology.Topo(sol, return_iter=False).faces
    for i, face in enumerate(the_faces):
        s = OCC.BRep.BRep_Tool.Surface(face) # make surface from face, get back handle
        t = CADhelpers.get_surface(s)
        print("{0} {1} {2} {3}".format(i, type(face), type(s), t))
        if "Geom_Plane" in t:
            the_wires = aocutils.topology.Topo(face, return_iter=False).wires
            if len(the_wires) == 2:
                wire0 = the_wires[0]
                wire1 = the_wires[1]

                edges0 = aocutils.topology.Topo(wire0, return_iter=False).edges
                edges1 = aocutils.topology.Topo(wire1, return_iter=False).edges

                e0 = edges0[0]
                e1 = edges1[0]

                c0, f0, l0 = OCC.BRep.BRep_Tool.Curve(e0)     # curve handle and first/last
                if not ("Geom_Circle" in CADhelpers.get_curve(c0)):
                    raise ValueError("something wrong with the Curve 0")
                c0 = OCC.Geom.Handle_Geom_Circle.DownCast(c0) # Downcast to circle handle
                c0 = c0.GetObject() # circle out of the handle
                k0 = CADhelpers.get_curve(c0)  # Get actual Geom Curve
                fp0 = c0.FirstParameter()
                lp0 = c0.LastParameter()
                r0  = c0.Radius()

                c1, f1, l1 = OCC.BRep.BRep_Tool.Curve(e1)     # curve handle and first/last
                if not ("Geom_Circle" in CADhelpers.get_curve(c1)):
                    raise ValueError("something wrong with the Curve 1")
                c1 = OCC.Geom.Handle_Geom_Circle.DownCast(c1) # Downcast to circle handle
                c1 = c1.GetObject() # circle out of the handle
                k1 = CADhelpers.get_curve(c1)  # Get actual Geom Curve
                fp1 = c1.FirstParameter()
                lp1 = c1.LastParameter()
                r1  = c1.Radius()

                print("  {0} {1} {2} {3} {4} {5}".format(fp0, lp0, r0, fp1, lp1, r1))

        elif t == "Geom_BSplineSurface":
            ss = CADhelpers.cast_surface(s).GetObject()
            print("  {0} {1} {2} {3}".format(i, type(ss), CADhelpers.get_surface(ss), t))

            if ss.IsUClosed() and ss.IsUPeriodic() and not ss.IsVClosed() and not ss.IsVPeriodic():
                print("    {0} {1} {2} {3}".format(ss.IsUClosed(), ss.IsUPeriodic(), ss.IsVClosed(), ss.IsVPeriodic()))
            else:
                continue

            U1, U2, V1, V2 = ss.Bounds()
            print("      {0} {1} {2} {3}".format(U1, U2, V1, V2))

            print(sep)
            pts, outline = compute_bspline_midline(ss, Nv = 220)
            if pts is None:
                raise RuntimeError("Something wrong with ")

            xfc, yfc, zfc      = convert_fiducial(pts, origin = -101.0)
            xow, yow, xiw, yiw = convert_outline(outline, origin = -101.0)

            for x, y, z in map(lambda x, y, z: (x,y,z), xfc, yfc, zfc) :
                print("        {0}    {1}    {2}".format(x, y, z))
            print(sep)
            for y, r in map(lambda x, y: (x,y), xow, yow):
                print("        {0}    {1}".format(y, r))
            print(sep)
            for y, r in map(lambda x, y: (x,y), xiw, yiw):
                print("        {0}    {1}".format(y, r))
            print(sep)

            iw = [point2d(np.float32(x), np.float32(y)) for x, y in zip(xiw, yiw)]
            iw = point2d.remove_dupes(iw, 0.5)

            ow = [point2d(np.float32(x), np.float32(y)) for x, y in zip(xow, yow)]
            ow = point2d.remove_dupes(ow, 0.5)

            fc = list(zip(xfc, yfc, zfc))
            fc = point3d.cvt2array(rdp(fc, 0.01))

            write_OCP(8, 1, 101, iw, ow, fc)

            break

            # the_wires = aocutils.topology.Topo(face, return_iter=False).wires

            # wire  = the_wires[0]
            # the_edges = aocutils.topology.Topo(wire, return_iter=False).edges

            # for j, edge in enumerate(the_edges):
            #     c, f, l = OCC.BRep.BRep_Tool.Curve(edge) # curve and first/last
            #     if "Geom_BSplineCurve" in CADhelpers.get_curve(c):

            #         c = OCC.Geom.Handle_Geom_BSplineCurve.DownCast(c).GetObject()

            #         fp = c.FirstParameter()
            #         lp = c.LastParameter()

            #         print("      ------------- {0} {1} {2} {3}".format(j, fp, lp, type(c)))

            #         step = (lp - fp)/100.0
            #         pt = OCC.gp.gp_Pnt()
            #         for k in range(0, 101):
            #             p = fp + step*float(k)
            #             t = c.D0(p, pt)
            #             print("      {0}  {1}  {2}".format(pt.X(), pt.Y(), pt.Z()))

#    print(sep)
#    the_edges = aocutils.topology.Topo(sol, return_iter=False).edges
#    for i, edge in enumerate(the_edges):
#        c, f, l = OCC.BRep.BRep_Tool.Curve(edge) # curve and
#        c = c.GetObject()
#        k = CADhelpers.get_curve(c)
#        print("{0} {1} {2} {3}".format( f, l, type(c), k ))

    sys.exit(0)
