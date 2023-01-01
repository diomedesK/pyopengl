import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def drawText(x, y, text):                                                
    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

pygame.init()
clock = pygame.time.Clock()

display = (400, 300)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
font = pygame.font.SysFont('arial', 64)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    drawText(140, 120, "2019")
    pygame.display.flip()

pygame.quit()
exit()
