from core.Attribute import Attribute

class Geometry(object):
    """Stores attribute data and the total number of vertices"""

    def __init__(self):
        super(Geometry, self).__init__()
        self.attributes = {}
        self.vertexCount = 0

    def addAttribute(self, dataType, name, data):
        self.attributes[name] = Attribute(dataType, data)

    def countVertices(self):
        self.vertexCount = len(list( self.attributes.values() )[0].data)
