import pygame, copy

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

        self.__mouseEventsNull = {
                MOUSE_MOTION        : None ,
                MOUSE_WHEEL         : None ,
                MOUSE_BUTTON_DOWN   : None ,
                MOUSE_BUTTON_UP     : None 
                }
        self.mouseEvents = {}

    def update(self):
        self.keyDownList = []
        self.keyUpList = []
            
        self.mouseEvents = copy.copy(self.__mouseEventsNull)

        for event in pygame.event.get():

            if ( event.type == pygame.MOUSEMOTION ):
                self.onMouseMotion(event)
                self.mouseEvents[MOUSE_MOTION] = event #pyright: ignore

            if event.type == pygame.MOUSEWHEEL:
                self.onMouseWheel(event)
                self.mouseEvents[MOUSE_WHEEL] = event #pyright: ignore

            if event.type == pygame.MOUSEBUTTONDOWN :
                self.onMouseButtonDown(event)
                self.mouseEvents[MOUSE_BUTTON_DOWN] = event #pyright: ignore

            if event.type == pygame.MOUSEBUTTONUP:
                self.onMouseButtonUp(event)
                self.mouseEvents[MOUSE_BUTTON_UP] = event #pyright: ignore

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
