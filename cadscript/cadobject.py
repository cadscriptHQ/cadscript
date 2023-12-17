import cadquery as cq


class CadObject:

    def __init__(self, workplane):
        self.wp = workplane

    def cq(self):
        return self.wp

    def fillet(self, edgesStr, amount):
        result = self.wp.edges(edgesStr).fillet(amount)
        self.wp = result
        return self

    def chamfer(self, edgesStr, amount):
        result = self.wp.edges(edgesStr).chamfer(amount)
        self.wp = result
        return self

    def move(self, translationVector):
        loc = cq.Location(cq.Vector(translationVector))
        c = self.wp.findSolid()
        c.move(loc)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def rotate(self, axis, degrees):
        c = self.wp.findSolid()
        if axis == "X":
            c = c.rotate((0,0,0),(1,0,0), degrees)
        elif axis == "Y":
            c = c.rotate((0,0,0),(0,1,0), degrees)
        elif axis == "Z":
            c = c.rotate((0,0,0),(0,0,1), degrees)
        else:
            raise ValueError("axis unknown")
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def cut(self, cad2):
        c1 = self.wp.findSolid()
        c2 = cad2.wp.findSolid()
        c = c1.cut(c2)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def fuse(self, cad2):
        c1 = self.wp.findSolid()
        c2 = cad2.wp.findSolid()
        c = c1.fuse(c2)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def add_extrude(self, faceStr, sketch, amount):
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "a")
        self.wp = result
        return self

    def cut_extrude(self, faceStr, sketch, amount):
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "s")
        self.wp = result
        return self

    def make_extrude(self, faceStr, sketch, amount):
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, False)
        c = result.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)

    def CenterOfBoundBox(self):
        c = self.wp.findSolid()
        shapes = []
        for s in c:
            shapes.append(s)
        return cq.Shape.CombinedCenterOfBoundBox(shapes)

    def copy(self):
        c = self.wp.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)

    def export_step(self, filename):
        self.wp.findSolid().exportStep(filename)

    def export_stl(self, filename):
        self.wp.findSolid().exportStl(filename)

    def render_svg(self, filename):
        c = self.wp.findSolid()
        cq.exporters.export(c,
                            filename,
                            opt={
                                "width": 300,
                                "height": 300,
                                "marginLeft": 10,
                                "marginTop": 10,
                                "showAxes": False,
                                "projectionDir": (1, 1, 1),
                                "strokeWidth": 0.8,
                                "strokeColor": (0, 0, 0),
                                "hiddenColor": (0, 0, 255),
                                "showHidden": False,
                            },)