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
    def __init__(self, drag = 1.0):
        super(MovementRig, self).__init__()
        
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

    def update(self, inputObject, moveAmount):

        a = self.lookAttachment.transform.item( ( 0, 0 )) 
        b = self.lookAttachment.transform.item( ( 0, 2 ))
        deltaX, deltaZ = -math.copysign(b**2, b), +math.copysign(a**2, a),
        
        availableMouseEvents = list(filter( lambda e : e != None, inputObject.mouseEvents.values() ))

        for event in availableMouseEvents:
            if ( event.type == pygame.MOUSEMOTION ):
                self.lookAttachment.rotateY( self.getTurnAmount( -event.rel[0]) * 1)
                self.lookAttachment.rotateX( self.getTurnAmount( -event.rel[1]) * 1)

            if event.type == pygame.MOUSEWHEEL:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN :
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                pass


        for key in inputObject.keyPressedList:
            ## VIEW CAMERA TRANSLATIONS ##

            if key == "w":
                self.translate(deltaX * moveAmount, 0, -deltaZ * moveAmount, False)
            if key == "s":
                self.translate(-deltaX * moveAmount, 0, +deltaZ * moveAmount, False)
            if key == "a":
                self.translate(-deltaZ * moveAmount, 0, -deltaX * moveAmount, False)
            if key == "d":                              
                self.translate(+deltaZ * moveAmount, 0, +deltaX * moveAmount, False)

            if key == "q":
                self.translate(0, -moveAmount, 0, False)
            if key == "e":
                self.translate(0, +moveAmount, 0, False)
    
