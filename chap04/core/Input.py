import pygame

MOUSE_MOTION = "mouseMotion"
MOUSE_WHEEL = "mouseWheel"
MOUSE_BUTTON_UP = "mouseButtonUp"
MOUSE_BUTTON_DOWN = "mouseButtonDown"

class Input(object):

    def __init__(self, controller):
        self.controller = controller

        self.keyDownList = []
        self.keyUpList = []
        self.keyPressedList = []

        self.mouseEvents = {}

        self.onMouseMotion = lambda event : event
        self.onMouseWheel = lambda event : event
        self.onMouseButtonDown = lambda event : event
        self.onMouseButtonUp = lambda event : event



    def update(self):
        self.keyDownList = []
        self.keyUpList = []
        

        for event in pygame.event.get():

            if ( event.type == pygame.MOUSEMOTION ):
                self.onMouseMotion(event)

            if event.type == pygame.MOUSEWHEEL:
                self.onMouseWheel(event)

            if event.type == pygame.MOUSEBUTTONDOWN :
                self.onMouseButtonDown(event)

            if event.type == pygame.MOUSEBUTTONUP:
                self.onMouseButtonUp(event)

            if event.type == pygame.QUIT:
                self.controller.running = False
            
            if event.type == pygame.KEYDOWN:
                key_name =  (pygame.key.name(event.key)) 
                self.keyDownList.append(key_name)
                self.keyPressedList.append(key_name)

            if event.type == pygame.KEYUP:
                key_name =  (pygame.key.name(event.key)) 
                self.keyUpList.append(key_name)
                self.keyPressedList.remove(key_name)

    def isKeyDown(self, key_name):
        return key_name in self.keyDownList

    def isKeyUp(self, key_name):
        return key_name in self.keyUpList

    def isKeyPressed(self, key_name):
        return key_name in self.keyPressedList
