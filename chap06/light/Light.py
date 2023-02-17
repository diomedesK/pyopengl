from core.Object3D import Object3D

class Light(Object3D):
    """docstring for Light"""
        
    AMBIENT = 1
    DIRECTIONAL = 2 
    POINT = 3

    def __init__(self, lightType = 0):
        super(Light, self).__init__()
        self.lightType = lightType
        self.attenuation = [1, 0, 0]
        self.color = [1, 1, 1]
        
