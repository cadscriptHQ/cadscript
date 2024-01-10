# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadquery as cq

class NearestToPointListSelector(cq.Selector):
    """
    for each of the provided points, select the nearest one.

    Similar to cq.NearestToPointSelector, but for multiple points.

    """

    def __init__(self, pnt_list):
        self.pnt_list = pnt_list

    def filter(self, objectList):
        def dist(tShape, pnt):
            return tShape.Center().sub(cq.Vector(*pnt)).Length
            # if tShape.ShapeType == 'Vertex':
            #    return tShape.Point.sub(toVector(self.pnt)).Length
            # else:
            #    return tShape.CenterOfMass.sub(toVector(self.pnt)).Length

        return [min(objectList, key=lambda tShape: dist(tShape, pnt)) for pnt in self.pnt_list]
