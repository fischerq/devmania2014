from fysom import Fysom
from pygame.locals import *
import resources

class Menu:
    def __init__(self, display):
        self.display = display
        self.fsm = Fysom({ 'initial': 'start',
            'events': [
                {'name': 'up', 'src': 'credits', 'dst': 'start'},
                {'name': 'up', 'src': 'start', 'dst': 'credits'},
                {'name': 'down', 'src': 'start', 'dst': 'credits'},
                {'name': 'down', 'src': 'credits', 'dst': 'start'}] })

    def processInput(self, event):
        if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return "enter"
                elif event.key == K_UP:
                    return "up"
                elif event.key == K_DOWN:
                    return "down"
        return None

    def update(self, commands):
        for command in commands:
            if command == "enter":
                return self.fsm.current
            else:
                self.fsm.trigger(command)
        return None

    def render(self):
        color = (0, 0, 0)
        textSurface = resources.get("basicFont").render('Menu', True, color, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = self.display.get_rect().centerx
        textRect.centery = self.display.get_rect().centery - 50
        self.display.blit(textSurface, textRect)

        if self.fsm.current == "start":
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)
        textSurface = resources.get("basicFont").render('Start', True, color, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.right = self.display.get_rect().centerx -  10
        textRect.centery = self.display.get_rect().centery + 30
        self.display.blit(textSurface, textRect)

        if self.fsm.current == "credits":
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)
        textSurface = resources.get("basicFont").render('Credits', True, color, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.left = self.display.get_rect().centerx +  10
        textRect.centery = self.display.get_rect().centery + 30
        self.display.blit(textSurface, textRect)