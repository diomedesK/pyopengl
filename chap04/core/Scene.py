from core.Object3D import Object3D

class Scene(Object3D):
    """The root node for the scene graph"""

    def __init__(self):
        super(Scene, self).__init__()
        
