# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadscript as cad

# create set of rummy game tokens
# numbered 1 to 13

height = 3.5  # mm


def base():
    # create a box, centered around origin
    body = cad.make_box(24, 36, height, center=True)
    # fillet on all edges parallel to Z axis
    body.fillet("|Z", 3)
    # chamfer on all edges orthogonal to Z axis
    body.chamfer("#Z", 0.6)
    return body


def gameToken(number):
    # create text geometry
    t1 = cad.make_text(number, 18, 5, font="Cooper Black")
    # center it in x, move to right pos in y and z
    (cx, cy, _) = t1.get_center()
    t1.move((-cx, 9 - cy, 1))
    # make a copy, rotate its
    t2 = t1.copy().rotate("Z", 180)
    # make base token, cut text from it
    return base().cut(t1).cut(t2)


def exportAll():
    ''' create game tokens 1 to 13, save them as STL files '''
    for i in range(1, 14):
        number = str(i)
        s = gameToken(number)
        s.export_stl("build/rummy_" + number + ".stl")


cad.show(gameToken("13"))
