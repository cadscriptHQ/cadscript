import cadquery as cq
from .cadobject import CadObject

class Assembly:

    def __init__(self):
        self.assy = cq.Assembly()

    def cq(self):
        return self.assy

    def add(self, part: CadObject):
        self.assy.add(part.cq())
        return self.assy