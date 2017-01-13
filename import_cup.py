# coding: utf-8

from __future__ import print_function

import sys
import logging

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

def main(fname):
    """
    Given the file name, read STEP from it and display it
    """

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

    shapes = readSTEP(fname)

    print("Nb shapes: %i" % len(shapes))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for shape in shapes:
        print(shape.ShapeType())  # 2 -> solid
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(shapes[0])
    print(dir(shapes[0]))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    display_shapes(shapes)

if __name__ == "__main__":

    main("cups/XMSGP030A10.01-003 breast_cup_outer_S fiducial wire.STEP") # "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP"

    sys.exit(0)
