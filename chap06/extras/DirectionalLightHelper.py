from extras.GridHelper import GridHelper

class DirectionalLightHelper(GridHelper):
    """docstring for DirectionalLightHelper"""
    def __init__(self, directionalLight):
        color = directionalLight.color
        super(DirectionalLightHelper, self).__init__(size=1, divisions=4, color=color)

        self.geometry.attributes["vertexPosition"].data += [[0, 0, 0,], [0, 0, -10]]
        self.geometry.attributes["vertexColor"].data += [color, color]

        self.geometry.attributes["vertexPosition"].uploadData()
        self.geometry.attributes["vertexColor"].uploadData()

        self.geometry.countVertices()
