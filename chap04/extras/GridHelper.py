from core.Mesh import Mesh
from core.Geometry import Geometry
from materials.LineMaterial import LineMaterial


class GridHelper(Mesh):
    def __init__(self, size=10, divisions=10, gridColor = [1,1,1], centerColor = [0.5, 0.5, 0.5], lineWidth=1):
        geo = Geometry()
        positionData = []
        colorData = []

        #create range of values
        values = []
        deltaSize = size / divisions

        for n in range(divisions+1):
            values.append(-size*0.5+n*deltaSize)
            print(values[len(values) - 1])
        
        #add vertical lines
        for x in values:
            positionData.append([x, -size*0.5, 0])
            positionData.append([x, size*0.5, 0])

            if x == 0:
                colorData.append(centerColor)
                colorData.append(centerColor)
            else:
                colorData.append(gridColor)
                colorData.append(gridColor)
        

        #add horizontal lines
        for y in values:
            positionData.append([-size*0.5, y, 0])
            positionData.append([size*0.5, y, 0])
            
            if y == 0:
                colorData.append(centerColor)
                colorData.append(centerColor)
            else:
                colorData.append(gridColor)
                colorData.append(gridColor)

        geo.addAttribute("vec3", "vertexPosition", positionData)
        geo.addAttribute("vec3", "vertexColor", colorData)
        geo.countVertices()
        
        mat = LineMaterial(
            {
                "useVertexColors":True,
                "lineWidth":lineWidth,
                "lineType":"segments"
            }
        )

        #initialize the mesh
        super().__init__(geo, mat)



      

