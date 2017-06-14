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
    aocutils.display.topology.edges(display, shape, transparency=0.8)
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
    the_edges = aocutils.topology.Topo(sol, return_iter=False).edges
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

def readSTEP(filename):
    """
    Given the STEP filename, read shapes from it
    """
    fname = aocxchange.utils.path_from_file(__file__, filename)
    importer = aocxchange.step.StepImporter(fname)

    return importer.shapes

def str_shape(sh_type):
    """
    Given the shape type, returns shape description
    """
    types = ["COMPOUND", "COMPSOLID", "SOLID", "SHELL", "FACE", "WIRE", "EDGE", "VERTEX"]
    return types[sh_type]

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

def factory_shapes(shape):
    """
    upgrade shape based on type
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

def main(filename):
    """
    process single cup from filename
    """
    shapes = readSTEP(filename)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Number of shapes: {0}".format(len(shapes)))
    for shape in shapes:
        print("{0}: {1}".format(shape.ShapeType(), str_shape(shape.ShapeType())))
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

def get_surface(surface):
    """
    Given surface, return what kind it is
    """
    surfaces = ["Geom_BezierSurface", "Geom_BSplineSurface", "Geom_RectangularTrimmedSurface",
                "Geom_ConicalSurface", "Geom_CylindricalSurface", "Geom_Plane", "Geom_SphericalSurface",
                "Geom_ToroidalSurface", "Geom_SurfaceOfLinearExtrusion", "Geom_SurfaceOfRevolution"]

    for s in surfaces:
        if surface.IsKind(s):
            return s

    return None

def get_curve(curve):
    """
    Given curve, return integer kind
    """
    curves = ["Geom_BezierCurve", "Geom_BSplineCurve", "Geom_TrimmedCurve", "Geom_Circle", "Geom_Ellipse", "Geom_Hyperbola", "Geom_Parabola"]
    for c in curves:
        if curve.IsKind(c):
            return c

    return None

if __name__ == "__main__":

    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

    sol = main("cups/XMSGP030A10.01-003 breast_cup_outer_S fiducial wire.STEP") # "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP"

    #backend = aocutils.display.defaults.backend
    #display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)
    #display_all(display, sol)
    #start_display()

    #print_flags(sol)

    sep = "          -------------               "
    print(sep)
    print_all(sol, sep)
    print(sep)

    the_faces = aocutils.topology.Topo(sol, return_iter=False).faces
    for i, face in enumerate(the_faces):
        s = OCC.BRep.BRep_Tool.Surface(face) # make surface from face, get back handle
        s = s.GetObject()                    # actual object
        t = get_surface(s)
        print("{0} {1} {2} {3}".format(i, type(face), type(s), t))
        if t == "Geom_Plane":
            the_wires = aocutils.topology.Topo(face, return_iter=False).wires
            if len(the_wires) == 2:
                wire0 = the_wires[0]
                wire1 = the_wires[1]

                edges0 = aocutils.topology.Topo(wire0, return_iter=False).edges
                edges1 = aocutils.topology.Topo(wire1, return_iter=False).edges

                e0 = edges0[0]
                e1 = edges1[0]

                c0, f0, l0 = OCC.BRep.BRep_Tool.Curve(e0) # curve and first/last
                c0 = c0.GetObject() # Get handle of the Geom Curve
                k0 = get_curve(c0)  # Get actual Geom Curve
                fp = c0.FirstParameter()
                lp = c0.LastParameter()

                step = (lp - fp)/100.0
                pt = OCC.gp.gp_Pnt()
                for k in range(0, 101):
                    p = fp + step*float(k)
                    t = c0.D0(p, pt )
                    # print("      {0}  {1}  {2}".format(pt.X(), pt.Y(), pt.Z()))

                c1, f1, l1 = OCC.BRep.BRep_Tool.Curve(e0) # curve and first/last
                c1 = c1.GetObject() # Get handle of the Geom Curve
                k1 = get_curve(c1)  # Get actual Geom Curve

        if t == "Geom_BSplineSurface":
            the_wires = aocutils.topology.Topo(face, return_iter=False).wires

            wire  = the_wires[0]
            the_edges = aocutils.topology.Topo(wire, return_iter=False).edges

            for j, edge in enumerate(the_edges):
                c, f, l = OCC.BRep.BRep_Tool.Curve(edge) # curve and first/last
                c = c.GetObject() # Get handle of the Geom Curve
                a = get_curve(c)  # Get actual Geom Curve
                if a == "Geom_BSplineCurve":
                    fp = c.FirstParameter()
                    lp = c.LastParameter()

                    step = (lp - fp)/100.0
                    pt = OCC.gp.gp_Pnt()
                    print("      ------------- {0} {1} {2}".format(j, fp, lp))
                    for k in range(0, 101):
                        p = fp + step*float(k)
                        t = c.D0(p, pt)
                        print("      {0}  {1}  {2}".format(pt.X(), pt.Y(), pt.Z()))

#    print(sep)
#    the_edges = aocutils.topology.Topo(sol, return_iter=False).edges
#    for i, edge in enumerate(the_edges):
#        c, f, l = OCC.BRep.BRep_Tool.Curve(edge) # curve and
#        c = c.GetObject()
#        k = get_curve(c)
#        print("{0} {1} {2} {3}".format( f, l, type(c), k ))

    sys.exit(0)
