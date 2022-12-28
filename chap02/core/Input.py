import pygame

class Input(object):

    def __init__(self, controller):
        self.controller = controller

        self.keyDownList = []
        self.keyUpList = []
        self.keyPressedList = []

    def update(self):
        self.keyDownList = []
        self.keyUpList = []

        for event in pygame.event.get():
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
