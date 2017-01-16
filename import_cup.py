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

def display_shapes(shapes):
    """
    for list of shapes, display first one
    """

    backend = aocutils.display.defaults.backend
    display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)

    aocutils.display.topology.solids(display, shapes[0], transparency=0.8)
    aocutils.display.topology.edges(display, shapes[0])
    display.FitAll()
    display.View_Iso()
    start_display()

def readSTEP(fname):
    """
    Given the STEP filename, read shapes from it
    """

    filename = aocxchange.utils.path_from_file(__file__, fname)
    importer = aocxchange.step.StepImporter(filename)

    return importer.shapes

def str_shape(sh_type):
    """
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

def main(fname):
    """
    Given the file name, read STEP from it and display it
    """

    shapes = readSTEP(fname)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Nb shapes: %i" % len(shapes))
    for shape in shapes:
        print(str_shape(shape.ShapeType()))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(shapes[0])
    # print(dir(shapes[0]))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    return shapes

if __name__ == "__main__":

    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

    shapes = main("cups/XMSGP030A10.01-003 breast_cup_outer_S fiducial wire.STEP") # "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP"

    # display_shapes(shapes)

    sys.exit(0)
