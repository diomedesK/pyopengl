from light.Light import Light

class AmbientLight(Light):
    """docstring for AmbientLight"""
    def __init__(self, color = [1, 1, 1]):
        super().__init__(Light.AMBIENT)
        self.color = color
        
