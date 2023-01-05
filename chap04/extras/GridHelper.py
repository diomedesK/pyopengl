from core.Mesh import Mesh
from core.Geometry import Geometry

from materials.BasicMaterial import BasicMaterial
from materials.LineMaterial import LineMaterial

from OpenGL.GL import GL_LINES
from math import radians

class GridHelper(Mesh):
    """ Grid-plane shape for helping in 3D visualization"""
    def __init__(self, divisions = 10, size = 10, defaultColor = [1, 1, 1], lineWidth = 1):

        unitSize = size / divisions

        values = []
        positionData = []
        colorData = []

        for n in range( divisions + 1 ):
            values.append( -size/2 + n * unitSize )

        for x in values:
            positionData.append([x, -size/2, 0 ])
            positionData.append([x, +size/2, 0 ])

            colorData.append(defaultColor)

        for y in values:
            positionData.append([-size/2, y, 0 ])
            positionData.append([+size/2, y, 0 ])

            colorData.append(defaultColor)

        geo = Geometry()
        geo.addAttribute("vec3", "vertexPosition", positionData)
        geo.addAttribute("vec3", "vertexColor", colorData)
        geo.countVertices()

        mat = LineMaterial()
        mat.settings["drawStyle"] = GL_LINES
        mat.settings["lineWidth"] = lineWidth
        mat.addUniform("bool", "useBaseColorOnly", True)
        mat.locateUniforms()

        super().__init__(geo, mat)
        

