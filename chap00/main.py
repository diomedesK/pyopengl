from core.Attribute import Attribute
from core.OpenGLUtils import OpenGLUtils

import pygame

class Main(object):
    def __init__(self):
        super(Main, self).__init__()
        pygame.init()
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL

        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLESAMPLES, 4)

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.mouse.set_pos((400, 300))


        self.screen = pygame.display.set_mode( [512, 512], displayFlags )
        pygame.display.set_caption("System32")

        vs = """
        uniform mat4 viewMatrix;
        uniform mat4 projMatrix;

        void main(){
            gl_Position = vec4(0.0, 0.2, 0.0, 1.0);
        }
        """

        fs = """
        out vec4 fragColor;
        void main(){
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }
        """

        OpenGLUtils.initializeProgram(vs, fs)

Main()
