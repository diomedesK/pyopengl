from core.Mesh import Mesh
from core.Geometry import Geometry
from materials.LineMaterial import LineMaterial

class AxesHelper(Mesh):
    """ Auxiliary shape for identifying 3D axis """
    def __init__(self, axisLength = 2, lineWidth = 2, axisColors = [ [1, 0, 0], [ 0, 1, 0 ], [0, 0, 1] ]):

        geo = Geometry()
        mat = LineMaterial({
            "lineWidth": lineWidth
            })

        positions = [
                [0, 0, 0], [axisLength, 0, 0], 
                [0, 0, 0], [0, axisLength, 0], 
                [0, 0, 0], [0, 0, axisLength], 
                ]

        colors = [
                axisColors[0], axisColors[0],
                axisColors[1], axisColors[1],
                axisColors[2], axisColors[2],
                ]

        geo.addAttribute("vec3", "vertexPosition", positions)
        geo.addAttribute("vec3", "vertexColor", colors)
        geo.countVertices()

        mat.addUniform("bool", "useVertexColors", True)
        mat.addUniform("bool", "useBaseColorOnly", False)
        mat.locateUniforms()

        super(AxesHelper, self).__init__(geo, mat)
        
