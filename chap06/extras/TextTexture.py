from core.Texture import Texture
import pygame

class TextTexture(Texture):
    def __init__(self, text="Hello, world!", systemFontName="Arial", fontFileName=None, fontSize=24, fontColor=[0,0,0], backgroundColor=[255,255,255], transparent=False, imageWidth=None, imageHeight=None, alignHorizontal=0.0, alignVertical=0.0, imageBorderWidth=0, imageBorderColor=[0,0,0]):

        super().__init__()

        if fontFileName is None:
            font = pygame.font.SysFont(systemFontName, fontSize)
        else:
            font = pygame.font.Font(fontFileName, fontSize)

        fontSurface = font.render(text, True, fontColor)
        self.surface = pygame.Surface(( 244, 244 ), pygame.SRCALPHA)
        
        textWidth, textHeight = font.size(text)

        if imageWidth is None:
            imageWidth = textWidth

        if imageHeight is None:
            imageHeight = textHeight
        
        if not transparent:
            self.surface.fill(backgroundColor)

        cornerPoint = (alignHorizontal * ( imageWidth - textWidth )), (alignVertical * ( imageHeight - textHeight ))
        dest_rect = fontSurface.get_rect(topleft=cornerPoint)

        if imageBorderWidth > 0:
            pygame.draw.rect(self.surface, imageBorderColor, [0, 0, imageWidth, imageHeight], imageBorderWidth)

        self.surface.blit(fontSurface, dest_rect)

        self.uploadData()
        
