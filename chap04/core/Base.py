import pygame
from core.Input import Input

FRAME_RATE = 60

class Base(object):

    def __init__(self, screenSize=[512, 512]):
        #boiler plate code
        pygame.init()
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL

        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLESAMPLES, 4)

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        self.screen = pygame.display.set_mode( screenSize, displayFlags )
        pygame.display.set_caption("System32")

        self.running = True
        self.clock =  pygame.time.Clock()
        self.input = Input(self)

        self.timer = 0
        self.deltaTime = 0
        self.frameRate = FRAME_RATE

    def initialize(self):
        pass

    def update(self):
        pass

    def run(self):
        #idk why but the line below wont work if there's no pygame window
        #prob i didnt get what linking really means in graphics context
        self.initialize() 

        while self.running:
            self.input.update()

            #clock.get_time() returns the number of miliseconds elapsed since the last ticks
            # self.timer += self.clock.get_time() / 1000
            self.deltaTime = self.clock.get_time() / 1000
            self.timer +=  self.deltaTime 

            self.update()
            pygame.display.flip()
            self.clock.tick(self.frameRate)


        pygame.quit()
