# coding: utf-8

import sys
import logging
import math

from functools import partial

import OCC.TopoDS
import OCC.Display.SimpleGui

import aocutils.display.topology
import aocutils.display.backends

import aocxchange.step
import aocxchange.utils

from XcMath        import utils

from point2d       import point2d
from point3d       import point3d

import CADhelpers
import DISPhelpers

from XcIO.write_OCP  import write_OCP

def display_faces(display, shape, pattern: str, event = None) -> None:
    """
    Display shape faces given the display
    """
    transparency=0.8
    show_numbers=True
    numbers_height=20
    color_sequence = aocutils.display.color.prism_color_sequence

    display.EraseAll()

    the_faces = aocutils.topology.Topo(shape, return_iter=False).faces
    ais_context = display.GetContext().GetObject()

    for i, face in enumerate(the_faces):
        s = OCC.BRep.BRep_Tool.Surface(face).GetObject() # make surface from face, get back handle
        t = CADhelpers.get_surface(s)
        if pattern not in t:
            continue

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
    dfaces_bezier =  partial(display_faces, display, shape, "Geom_BezierSurface")
    dfaces_bezier.__name__ = "Bezier"
    dfaces_bspline = partial(display_faces, display, shape, "Geom_BSplineSurface")
    dfaces_bspline.__name__ = "BSpline"
    dfaces_conical = partial(display_faces, display, shape, "Geom_ConicalSurface")
    dfaces_conical.__name__ = "Conical"
    dfaces_cylindrical = partial(display_faces, display, shape, "Geom_CylindricalSurface")
    dfaces_cylindrical.__name__ = "Cylindrical"
    dfaces_spherical = partial(display_faces, display, shape, "Geom_SphericalSurface")
    dfaces_spherical.__name__ = "Spherical"
    dfaces_plane =  partial(display_faces, display, shape, "Geom_Plane")
    dfaces_plane.__name__ = "Plane"
    dfaces_toro =  partial(display_faces, display, shape, "Geom_ToroidalSurface")
    dfaces_toro.__name__ = "Toro"
    dfaces_rect = partial(display_faces, display, shape, "Geom_RectangularTrimmedSurface")
    dfaces_rect.__name__ = "RecT"
    dfaces_linext = partial(display_faces, display, shape, "Geom_SurfaceOfLinearExtrusion")
    dfaces_linext.__name__ = "LinExt"
    dfaces_surfrev = partial(display_faces, display, shape, "Geom_SurfaceOfRevolution")
    dfaces_surfrev.__name__ = "SurfRev"
    add_function_to_menu('faces', dfaces_bezier)
    add_function_to_menu('faces', dfaces_conical)
    add_function_to_menu('faces', dfaces_cylindrical)
    add_function_to_menu('faces', dfaces_spherical)
    add_function_to_menu('faces', dfaces_bspline)
    add_function_to_menu('faces', dfaces_plane)
    add_function_to_menu('faces', dfaces_toro)
    add_function_to_menu('faces', dfaces_rect)
    add_function_to_menu('faces', dfaces_linext)
    add_function_to_menu('faces', dfaces_surfrev)
    add_menu('shells')
    dshells = partial(DISPhelpers.display_shells, display, shape)
    dshells.__name__ = "dshells"
    add_function_to_menu('shells', dshells)
    add_menu('wires')
    dwires = partial(DISPhelpers.display_wires, display, shape)
    dwires.__name__ = "dwires"
    add_function_to_menu('wires', dwires)


def readSTEP(filename: str):
    """
    Given the STEP filename, read shapes from it
    """
    fname = aocxchange.utils.path_from_file(__file__, filename)
    importer = aocxchange.step.StepImporter(fname)

    return importer.shapes

def main(filename: str):
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

def make_cup_shell(surfaces):
    """
    Given list of surfaces, computes and returns (y, r) tuple of the cup shell
    """
    sphere = surfaces[0]
    cone   = surfaces[1]
    top    = surfaces[2]

    print("Q {0} {1} {2}".format(type(sphere), type(cone), type(top)))

    U1s, U2s, V1s, V2s = sphere.Bounds()
    U1c, U2c, V1c, V2c = cone.Bounds()
    U1t, U2t, V1t, V2t = top.Bounds()

    # print("QA {0} {1} {2} {3}".format(U1s, U2s, V1s, V2s))
    # print("QB {0} {1} {2} {3}".format(U1c, U2c, V1c, V2c))
    # print("QC {0} {1} {2} {3}".format(U1t, U2t, V1t, V2t))

    rc = list()
    yc = list()

    pt = OCC.gp.gp_Pnt()

    # determine where spehre ends
    u = 0.0
    v = V1c
    cone.D0(u, v, pt)
    ymin = pt.Y()

    # sphere first
    Nv = 40
    u = math.pi / 2.0
    ve = 0.5*(V1s + V2s)
    for k in range(0, Nv+1):
        v = utils.clamp(V1s + float(k)*(ve - V1s)/float(Nv), V1s, V2s)
        sphere.D0(u, v, pt)
        if pt.Y() > ymin:
            continue
        # insert in reverse order
        yc.insert(0, pt.Y())
        rc.insert(0, pt.Z())

    # cone
    u = 0.0
    for k in range(0, Nv+1):
        v = utils.clamp(V1c + float(k)*(V2c - V1c)/float(Nv), V1c, V2c)
        cone.D0(u, v, pt)
        yc.append(pt.Y())
        rc.append(pt.Z())

    # top
    Nv = 4
    u = 0.0
    for k in range(0, Nv+1):
        v = utils.clamp(V1t + float(k)*(V2t - V1t)/float(Nv), V1t, V2t)
        top.D0(u, v, pt)
        yc.append(pt.Y())
        rc.append(pt.Z())

    # print("rrr {0} {1} {2}".format((U1s, U2s, V1s, V2s), (U1c, U2c, V1c, V2c), (U1t, U2t, V1t, V2t)) )
    return (yc, rc)

def write_ICP(RU, OuterCup, InnerCup, shift, yiw, riw, yow, row):
    """
    write to stdout ICP file
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
    sys.stdout.write(RU)
    sys.stdout.write("\n")

    # Outer cup
    sys.stdout.write(OuterCup)
    sys.stdout.write("\n")

    # Inner cup
    sys.stdout.write(InnerCup)
    sys.stdout.write("\n")

    # nof points in the inner wall
    niw = len(riw)
    if niw != len(yiw):
        return None
    sys.stdout.write(str(niw))
    sys.stdout.write("\n")

    # outer wall
    for r, y in zip(riw, yiw):
        sys.stdout.write("{0:13.6e} {1:13.6e}\n".format(shift - y, r))

    # nof points in the outer wall
    now = len(row)
    if now != len(yow):
        return None
    sys.stdout.write(str(now))
    sys.stdout.write("\n")

    # outer wall
    for r, y in zip(row, yow):
        sys.stdout.write("{0:13.6e} {1:13.6e}\n".format(shift - y, r))


if __name__ == "__main__":

    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

    sol = main("cups/XMSGP030A10.02-036 NS04.STEP") # "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP" # "cups/XMSGP030A10.01-003 breast_cup_outer_S 214.STEP"

    # backend = aocutils.display.defaults.backend
    # display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)
    # display_all(display, sol)
    # start_display()

    #CADhelpers.print_flags(sol)

    sep: str = "          -------------               "
    #print(sep)
    #CADhelpers.print_all(sol, sep)
    #print(sep)

    the_faces = aocutils.topology.Topo(sol, return_iter=False).faces

    outer = list()
    inner = list()

    for i, face in enumerate(the_faces):
        s = OCC.BRep.BRep_Tool.Surface(face) # get handle to the surface
        t = CADhelpers.get_surface(s)
        print("{0} {1} {2} {3}".format(i, type(face), type(s), t))

        if "Geom_SphericalSurface" in t:
            ss = CADhelpers.cast_surface(s).GetObject() # specific surface
            sphere = ss.Sphere()
            ssl = sphere.Location()
            ssp = sphere.Position()
            print("  {0} {1} {2} {3}".format(sphere.Radius(), ssl.X(), ssl.Y(), ssl.Z()))
            U1, U2, V1, V2 = ss.Bounds()
            print("    {0} {1} {2} {3}".format(U1, U2, V1, V2))

            blocks = CADhelpers.surface2gnuplot(ss)
            CADhelpers.save_gnuplot_surface("sphere", i, blocks, True)

        elif "Geom_ConicalSurface" in t:
            ss = CADhelpers.cast_surface(s).GetObject() # specific surface
            cone = ss.Cone()
            blocks = CADhelpers.surface2gnuplot(ss)
            CADhelpers.save_gnuplot_surface("cone", i, blocks, True)

        elif "Geom_RectangularTrimmedSurface" in t:
            ss = CADhelpers.cast_surface(s).GetObject() # specific surface
            blocks = CADhelpers.surface2gnuplot(ss)
            CADhelpers.save_gnuplot_surface("trim", i, blocks, True)
            bs = CADhelpers.cast_surface(ss.BasisSurface()).GetObject()
            #if "Geom_ConicalSurface" in str(type(bs)):
            #    CADhelpers.save_gnuplot_surface("conet", i, blocks, True)

    # for S5 - 14, 0, 11
    outer.append(CADhelpers.cast_surface(OCC.BRep.BRep_Tool.Surface(the_faces[21])).GetObject())
    outer.append(CADhelpers.cast_surface(OCC.BRep.BRep_Tool.Surface(the_faces[0])).GetObject())
    outer.append(CADhelpers.cast_surface(OCC.BRep.BRep_Tool.Surface(the_faces[18])).GetObject())

    print(sep)

    for k, o in enumerate(outer):
        t = CADhelpers.get_surface(o)
        print("{0} {1} {2}".format(k, type(o), t))
    print(sep)

    yow, row  = make_cup_shell(outer)

    print(sep)

    # for S5 - 15, 16, 09
    inner.append(CADhelpers.cast_surface(OCC.BRep.BRep_Tool.Surface(the_faces[22])).GetObject())
    inner.append(CADhelpers.cast_surface(OCC.BRep.BRep_Tool.Surface(the_faces[23])).GetObject())
    inner.append(CADhelpers.cast_surface(OCC.BRep.BRep_Tool.Surface(the_faces[16])).GetObject())

    for k, i in enumerate(inner):
        t = CADhelpers.get_surface(i)
        print("{0} {1} {2}".format(k, type(i), t))
    print(sep)

    yiw, riw = make_cup_shell(inner)

    print(sep)

    write_ICP("8", "1", "S04", -101.0, yiw, riw, yow, row)

    sys.exit(0)
