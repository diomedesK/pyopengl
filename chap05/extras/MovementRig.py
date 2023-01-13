from core.Object3D import Object3D
import pygame, math

class MovementRig(Object3D):
    
    # I was wondering why would it work out, but after some investigation i just rembmered
    # that the camera object, at each update() call, is modified according to the world transform,
    # which sums up the modifications of all its parents. 
    # tldr; it works because the camera object is added as a child of the lookAttachment
    
    ################ 

    # It's important that the camera be aligned to the origin in order to get 
    # first person illusion, otherwise a third person view is created.
    # The lookAttachment data is computed as part of the camera viewMatrix, and 
    # then uploaded to the GPU in the "viewCamera" GLSL uniform.

    """Tools for manipulating the view"""
    def __init__(self, drag = 1.0, userDefinedControls = {}):
        super(MovementRig, self).__init__()

        defaultControls = {
                "front"    : "w",
                "back"  : "s",
                "left"  : "a",
                "right" : "d",
                "up": "q",
                "down" : "e",
                }

        if userDefinedControls:
            self.controls = userDefinedControls
        else:
            self.controls = defaultControls
        
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self #pyright: ignore

        self.getTurnAmount = lambda coef : coef * math.radians( drag * 8 )


    def setLookPositionRelativeTo(self, obj : Object3D):
        self.lookAttachment.setPosition(obj.getPosition())
        
    def add(self, child):
        self.lookAttachment.add(child)
        
    def remove(self, child):
        self.lookAttachment.remove(child)

    def update(self, inputObject, moveAmount, ignoreMouseEvents = False, ignoreKeyboardEvents = False):

        a = self.lookAttachment.transform.item( ( 0, 0 )) 
        b = self.lookAttachment.transform.item( ( 0, 2 ))
        deltaX, deltaZ = -math.copysign(b**2, b), +math.copysign(a**2, a),

        availableMouseEvents = list(filter( lambda e : e != None, inputObject.mouseEvents.values() ))

        if not ignoreMouseEvents:

            for event in availableMouseEvents:
                if ( event.type == pygame.MOUSEMOTION ):
                    self.lookAttachment.rotateY( self.getTurnAmount( -event.rel[0]) * 1/100)
                    self.lookAttachment.rotateX( self.getTurnAmount( -event.rel[1]) * 1/100)

                    # self.lookAttachment.transform.itemset((1, 0), 0)
                    # self.lookAttachment.transform.itemset((0, 1), 0)

                if event.type == pygame.MOUSEWHEEL:
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN :
                    pass

                if event.type == pygame.MOUSEBUTTONUP:
                    pass


        if not ignoreKeyboardEvents:
            for key in inputObject.keyPressedList:
                ## VIEW CAMERA TRANSLATIONS ##


                if key == self.controls["front"]:
                    self.translate(deltaX * moveAmount, 0, -deltaZ * moveAmount, True)
                if key == self.controls["back"]:
                    self.translate(-deltaX * moveAmount, 0, +deltaZ * moveAmount, True)
                if key == self.controls["left"]:
                    self.translate(-deltaZ * moveAmount, 0, -deltaX * moveAmount, True)
                if key == self.controls["right"]:
                    self.translate(+deltaZ * moveAmount, 0, +deltaX * moveAmount, True)

                if key == self.controls["up"]:
                    self.translate(0, -moveAmount, 0, True)
                if key == self.controls["down"]:
                    self.translate(0, +moveAmount, 0, True)
    
