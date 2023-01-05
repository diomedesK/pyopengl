from core.Object3D import Object3D

class MovementRig(Object3D):
    
    # I was wondering why would it work out, but after some investigation i just rembmered
    # that the camera object, at each update() call, is modified according to the world transform,
    # which sums up the modifications of all its parents. 
    # tldr; it works because the camera object is added as a child of the lookAttachment

    """Tools for manipulating the view"""
    def __init__(self):
        super(MovementRig, self).__init__()
        
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self #pyright: ignore

    def add(self, child):
        self.lookAttachment.add(child)

    def remove(self, child):
        self.lookAttachment.remove(child)

    def update(self, inputObject, moveAmount):

        for key in inputObject.keyPressedList:

            ## VIEW CAMERA TRANSLATIONS ##

            if key == "w":
                self.lookAttachment.translate(0, 0, -moveAmount, False)
            if key == "s":
                self.lookAttachment.translate(0, 0, +moveAmount, False)
            if key == "a":
                self.lookAttachment.translate(-moveAmount, 0, 0, False)
            if key == "d":                              
                self.lookAttachment.translate(+moveAmount, 0, 0, False)

            if key == "q":
                self.lookAttachment.translate(0, +moveAmount, 0, False)
            if key == "e":
                self.lookAttachment.translate(0, -moveAmount, 0, False)
    
