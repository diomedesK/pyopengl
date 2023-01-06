from core.Object3D import Object3D
from core.Camera import Camera
import pygame, math

class MovementRig(Object3D):
    
    # I was wondering why would it work out, but after some investigation i just rembmered
    # that the camera object, at each update() call, is modified according to the world transform,
    # which sums up the modifications of all its parents. 
    # tldr; it works because the camera object is added as a child of the lookAttachment

    """Tools for manipulating the view"""
    def __init__(self, drag = 1.0):
        super(MovementRig, self).__init__()
        
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self #pyright: ignore

        self.cameraDescendant = None

        self.getTurnAmount = lambda coef : coef * math.radians( drag * 8 )
        self.onMouseMotion = lambda event, camera: (
                camera.rotateY( self.getTurnAmount( -event.rel[0]) * 1),
                camera.rotateX( self.getTurnAmount( -event.rel[1]) * 1),
                )
        self.onMouseWheel = lambda event, camera: {}
        self.onMouseButtonUp = lambda event, camera: {}
        self.onMouseButtonDown = lambda event, camera: {}
        
    def add(self, child):
        self.lookAttachment.add(child)

        if isinstance(child, Camera):
            self.cameraDescendant = child

    def remove(self, child):
        self.lookAttachment.remove(child)

    def update(self, inputObject, moveAmount):

        if self.cameraDescendant == None:
            return

        a = self.cameraDescendant.transform.item( ( 0, 0 )) 
        b = self.cameraDescendant.transform.item( ( 0, 2 ))
        deltaX, deltaZ = -math.copysign(b**2, b), +math.copysign(a**2, a),
        
        availableMouseEvents = list(filter( lambda e : e != None, inputObject.mouseEvents.values() ))

        for event in availableMouseEvents:
            if ( event.type == pygame.MOUSEMOTION ):
                self.onMouseMotion(event, self.cameraDescendant)

            if event.type == pygame.MOUSEWHEEL:
                self.onMouseWheel(event, self.cameraDescendant)

            if event.type == pygame.MOUSEBUTTONDOWN :
                self.onMouseButtonDown(event, self.cameraDescendant )

            if event.type == pygame.MOUSEBUTTONUP:
                self.onMouseButtonUp(event, self.cameraDescendant)


        for key in inputObject.keyPressedList:
            ## VIEW CAMERA TRANSLATIONS ##

            if key == "w":
                self.lookAttachment.translate(deltaX * moveAmount, 0, -deltaZ * moveAmount, False)
            if key == "s":
                self.lookAttachment.translate(-deltaX * moveAmount, 0, +deltaZ * moveAmount, False)
            if key == "a":
                self.lookAttachment.translate(-deltaZ * moveAmount, 0, -deltaX * moveAmount, False)
            if key == "d":                              
                self.lookAttachment.translate(+deltaZ * moveAmount, 0, +deltaX * moveAmount, False)

            if key == "q":
                self.lookAttachment.translate(0, -moveAmount, 0, False)
            if key == "e":
                self.lookAttachment.translate(0, +moveAmount, 0, False)
    
