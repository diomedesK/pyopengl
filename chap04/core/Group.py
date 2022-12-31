from core.Object3D import Object3D

class Group(Object3D):
    """A general container for the scene graph"""

    def __init__(self):
        super(Group, self).__init__()
        
