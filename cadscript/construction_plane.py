
import cadquery as cq

class ConstructionPlane:

    __wp : cq.Workplane

    def __init__(self, wp:cq.Workplane):
        self.__wp = wp

    def cq(self):
        return self.__wp
    
