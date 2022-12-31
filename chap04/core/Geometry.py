from core.Attribute import Attribute

class Geometry(object):
    """stores attribute data and the total number of vertices"""

    # stores Attribute objects in the class attribute dictionary.
    # After all of them are added, they are linked to the material program
    # indexed in the material varaible of the Mesh class

    def __init__(self):
        super(Geometry, self).__init__()
        self.attributes = {}
        self.vertexCount = None

    def addAttribute(self, dataType, variableName, data):
        self.attributes[variableName] = Attribute(dataType, data)

    def countVertices(self):
        # "number of vertices may be calculated from the length of any attribute object's array of data"
        # remember, it is an array of Attribute objects, so we pick-up the first one that appears and 
        # caculate the length of it's data varaible
        self.vertexCount =  len(list(self.attributes.values())[0].data)

