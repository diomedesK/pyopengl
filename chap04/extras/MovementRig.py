from core.Object3D import Object3D
import math 

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

        camera = self.lookAttachment.children[0]
        a = camera.transform.item( ( 0, 0 )) 
        aa = camera.transform.item( ( 2, 2 )) 

        b = camera.transform.item( ( 0, 2 ))
        bb = camera.transform.item( ( 2, 0 ))

        x_ = b**2 
        z_ = a**2

        xx, zz = -math.copysign(x_, b), +math.copysign(z_, a),

        for key in inputObject.keyPressedList:
            ## VIEW CAMERA TRANSLATIONS ##

            if key == "w":
                # self.lookAttachment.translate(0, 0, -moveAmount, False)
                self.lookAttachment.translate(xx * moveAmount, 0, -zz * moveAmount, False)
            if key == "s":
                # self.lookAttachment.translate(0, 0, +moveAmount, False)
                self.lookAttachment.translate(-xx * moveAmount, 0, +zz * moveAmount, False)
            if key == "a":
                self.lookAttachment.translate(-zz * moveAmount, 0, -xx * moveAmount, False)
            if key == "d":                              
                self.lookAttachment.translate(+zz * moveAmount, 0, +xx * moveAmount, False)

            if key == "q":
                self.lookAttachment.translate(0, -moveAmount, 0, False)
            if key == "e":
                self.lookAttachment.translate(0, +moveAmount, 0, False)
    
