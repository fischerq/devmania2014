import resources
from pygame.locals import *


class Credits:
    def __init__(self, display):
        self.display = display
        self.offset = 0

    def processInput(self, event):
        if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "exit"
        return None

    def update(self, commands):
        for command in commands:
            if command == "exit":
                return "menu"
        return None

    def render(self):
        color = (0, 0, 0)
        textSurface = resources.get("basicFont").render('Credits', True, color, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = self.display.get_rect().centerx
        textRect.centery = self.display.get_rect().centery
        self.display.blit(textSurface, textRect)