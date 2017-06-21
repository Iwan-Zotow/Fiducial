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

def display_facesQ(display, shape, pattern, event = None):
    """
    Display shape faces given the display
    """
    display.EraseAll()
    aocutils.display.topology.faces(display, shape, transparency=0.8)
    display.FitAll()
    display.View_Iso()

def display_faces(display, shape, pattern, event = None):
    """
    Display shape faces given the display
    """
    transparency=0.8
    show_numbers=True
    numbers_height=20
    color_sequence = aocutils.display.color.prism_color_sequence

    display.EraseAll()

    the_faces = aocutils.topology.Topo(shape, return_iter=False).faces
    print("{0} face(s) to display".format(len(the_faces)))
    ais_context = display.GetContext().GetObject()

    for i, face in enumerate(the_faces):
        s = OCC.BRep.BRep_Tool.Surface(face).GetObject() # make surface from face, get back handle
        t = CADhelpers.get_surface(s)
        if t != pattern:
            continue

        print("      {0} #{1}".format(pattern, i))
        ais_face = OCC.AIS.AIS_Shape(face)
        ais_face.SetColor(color_sequence[i % len(color_sequence)])
        ais_face.SetTransparency(transparency)
        if show_numbers:
            display.DisplayMessage(point=aocutils.brep.face.Face(face).midpoint,
                                   text_to_write = "{0}".format(i),
                                   height=numbers_height,
                                   message_color=(1, 0, 0))
        ais_context.Display(ais_face.GetHandle())

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
    dfaces_conical = partial(display_faces, display, shape, "Geom_ConicalSurface")
    dfaces_conical.__name__ = "Conical"
    dfaces_cylindrical = partial(display_faces, display, shape, "Geom_CylindricalSurface")
    dfaces_cylindrical.__name__ = "Cylindrical"
    dfaces_spherical = partial(display_faces, display, shape, "Geom_SphericalSurface")
    dfaces_spherical.__name__ = "Spherical"
    dfaces_bspline = partial(display_faces, display, shape, "Geom_BSplineSurface")
    dfaces_bspline.__name__ = "BSpline"
    dfaces_plane =  partial(display_faces, display, shape, "Geom_Plane")
    dfaces_plane.__name__ = "Plane"
    dfaces_toro =  partial(display_faces, display, shape, "Geom_ToroidalSurface")
    dfaces_toro.__name__ = "Toro"
    dfaces_rect = partial(display_faces, display, shape, "Geom_RectangularTrimmedSurface")
    dfaces_rect.__name__ = "RecT"
    add_function_to_menu('faces', dfaces_conical)
    add_function_to_menu('faces', dfaces_cylindrical)
    add_function_to_menu('faces', dfaces_spherical)
    add_function_to_menu('faces', dfaces_bspline)
    add_function_to_menu('faces', dfaces_plane)
    add_function_to_menu('faces', dfaces_toro)
    add_function_to_menu('faces', dfaces_rect)
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

def main(filename):
    """
    process single cup from filename
    """
    shapes = readSTEP(filename)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Number of shapes: {0}".format(len(shapes)))
    for shape in shapes:
        print("{0}: {1} {2}".format(shape.ShapeType(), CADhelpers.str_shape(shape.ShapeType()), type(aocutils.topology.shape_to_topology(shape))))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    sol = aocutils.topology.shape_to_topology(shape)

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

if __name__ == "__main__":

    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

    sol = main("cups/XMSGP030A10.01-003 breast_cup_outer_S 214.STEP") # "cups/XMSGP030A10.02-037 NS05 .STEP") # "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP"

    backend = aocutils.display.defaults.backend
    display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)
    display_all(display, sol)
    start_display()

    #print_flags(sol)

    sep = "          -------------               "
    #print(sep)
    #CADhelpers.print_all(sol, sep)
    #print(sep)

    the_faces = aocutils.topology.Topo(sol, return_iter=False).faces

    for i, face in enumerate(the_faces):
        s = OCC.BRep.BRep_Tool.Surface(face) # get handle to the surface
        t = CADhelpers.get_surface(s)
        print("{0} {1} {2} {3}".format(i, type(face), type(s), t))
        if "Geom_SphericalSurface" in t:
            rs = CADhelpers.cast_surface(s).GetObject()
            spl = rs.Location()
            spp = rs.Position()
            print("{0} {1} {2} {3}".format(rs.Radius(), spl.X(), spl.Y(), spl.Z()))

    sys.exit(0)
