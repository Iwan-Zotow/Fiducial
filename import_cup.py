#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import logging

import OCC.Display.SimpleGui

import aocutils.display.topology
import aocutils.display.backends

import aocxchange.step
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

backend = aocutils.display.defaults.backend
display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)

# filename = aocxchange.utils.path_from_file(__file__, "XMSGP030A10.01-003 breast_cup_outer_S 214.STEP")
filename = aocxchange.utils.path_from_file(__file__, "XMSGP030A10.01-003 breast_cup_outer_S fiducial wire.STEP")
step_importer = aocxchange.step.StepImporter(filename)

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(dir(step_importer))
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

print("Nb shapes: %i" % len(step_importer.shapes))
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
for shape in step_importer.shapes:
    print(shape.ShapeType())  # 2 -> solid
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(step_importer.shapes[0])
print(dir(step_importer.shapes[0]))
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# aocutils.display.topology.solids(display, step_importer.shapes[0], transparency=0.8)
# aocutils.display.topology.edges(display, step_importer.shapes[0])
# display.FitAll()
# display.View_Iso()
# start_display()
