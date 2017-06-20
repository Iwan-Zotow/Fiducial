# coding: utf-8

from __future__ import print_function

import sys
import logging

import OCC.TopoDS
import OCC.Display.SimpleGui

import aocutils.display.topology
import aocutils.display.backends

import aocxchange.step
import aocxchange.utils

import CADhelpers

from functools import partial

def display_solids(display, shape, event = None):
    """
    Display shape solids given the display
    """
    display.EraseAll()
    aocutils.display.topology.solids(display, shape, transparency=0.8)
    display.FitAll()
    display.View_Iso()

def display_faces(display, shape, event = None):
    """
    Display shape faces given the display
    """
    display.EraseAll()
    aocutils.display.topology.faces(display, shape, transparency=0.8)
    display.FitAll()
    display.View_Iso()

def display_shells(display, shape, event = None):
    """
    Display shape shells given the display
    """
    display.EraseAll()
    aocutils.display.topology.shells(display, shape, transparency=0.8)
    display.FitAll()
    display.View_Iso()

def display_edges(display, shape, event = None):
    """
    Display shape edges given the display
    """
    display.EraseAll()
    aocutils.display.topology.edges(display, shape)
    display.FitAll()
    display.View_Iso()

def display_wires(display, shape, event = None):
    """
    Display shape wires given the display
    """
    display.EraseAll()
    aocutils.display.topology.wires(display, shape)
    display.FitAll()
    display.View_Iso()

def display_all(display, shape):
    """
    display every part of the shape
    """
    add_menu('solids')
    dsolids = partial(display_solids, display, shape)
    dsolids.__name__ = "dsolids"
    add_function_to_menu('solids', dsolids)
    add_menu('edges')
    dedges = partial(display_edges, display, shape)
    dedges.__name__ = "dedges"
    add_function_to_menu('edges', dedges)
    add_menu('faces')
    dfaces = partial(display_faces, display, shape)
    dfaces.__name__ = "dfaces"
    add_function_to_menu('faces', dfaces)
    add_menu('shells')
    dshells = partial(display_shells, display, shape)
    dshells.__name__ = "dshells"
    add_function_to_menu('shells', dshells)
    add_menu('wires')
    dwires = partial(display_wires, display, shape)
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

def compute_bspline_midline(bspline, Nv = 100, Nu = 256):
    """
    Given the bspline surface with one open and one closed/periodic parameter,
    compute middle/center line assuming closed parameter is a circle

    Nu - number of points in U space, how much points will be returned
    Nv - number of points in V space, how much to use to compute middle point

    Returns array of 3d points
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

    rc = list()

    pt = OCC.gp.gp_Pnt()

    vstep = (V2 - V1) / float(Nv)
    ustep = (U2 - U1) / float(Nu)
    uwght = 1.0 / float(Nu)
    for kv in range(0, Nv+1):
        v = V1 + vstep * float(kv)
        x = 0.0
        y = 0.0
        z = 0.0
        for ku in range(0, Nu+1):
            u = U1 + ustep * float(ku)
            ss.D0(u, v, pt)
            x += pt.X()
            y += pt.Y()
            z += pt.Z()

        rc.append(OCC.gp.gp_Pnt(uwght*x, uwght*y, uwght*z))

    if len(rc) == 0:
        return None
    return rc

if __name__ == "__main__":

    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

    sep = "          -----------------             "
    sol = main("cups/XMSGP030A10.01-003 breast_cup_outer_S fiducial wire.STEP") # "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP"

    # backend = aocutils.display.defaults.backend
    # display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)
    # display_all(display, sol)
    # start_display()

    #print_flags(sol)

    print(sep)
    CADhelpers.print_all(sol, sep)
    print(sep)

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
            pts = compute_bspline_midline(ss)
            if pts is None:
                raise RuntimeError("Something wrong with ")
            for pt in pts:
                print("        {0}  {1}  {2}".format(pt.X(), pt.Y(), pt.Z()))
            print(sep)

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
