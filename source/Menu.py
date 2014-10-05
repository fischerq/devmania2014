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
        self.player_controllers = [None, None]

    def process_input(self, event):
        if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return "enter"
                elif event.key == K_UP:
                    return "up"
                elif event.key == K_DOWN:
                    return "down"
        if self.player_controllers[0] is None or self.player_controllers[1] is None:
            if event.type == JOYBUTTONDOWN and event.button == 9:
                if self.player_controllers[0] is None:
                    self.player_controllers[0] = event.joy
                elif self.player_controllers[1] is None and event.joy != self.player_controllers[0]:
                    self.player_controllers[1] = event.joy
                    resources.set("player_joysticks", self.player_controllers)

        elif event.type == JOYBUTTONDOWN and event.button == 9:
                    return "enter"
        return None

    def update(self, commands):
        for command in commands:
            if command == "enter":
                if self.player_controllers[0] is not None and self.player_controllers[1] is not None:
                    return self.fsm.current
                else:
                    return None
            else:
                self.fsm.trigger(command)
        return None

    def render(self):
        #self.display.blit(resources.get("imgBackgroundMenu"), (0, 0))

        self.display.blit(resources.get("imgMenuTitle"), (self.display.get_rect().centerx - resources.get("imgMenuTitle").get_width()/2, self.display.get_rect().centery - resources.get("imgMenuTitle").get_height()/2 - 200))

        if self.fsm.current == "start":
            color = (0, 0, 0)
        else:
            color = (220, 220, 220)
        text_surface = resources.get("basicFont").render('Start', True, color)
        text_rect = text_surface.get_rect()
        text_rect.right = self.display.get_rect().centerx -  10
        text_rect.centery = self.display.get_rect().centery - 100
        self.display.blit(text_surface, text_rect)

        if self.fsm.current == "credits":
            color = (0, 0, 0)
        else:
            color = (220, 220, 220)
        text_surface = resources.get("basicFont").render('Credits', True, color)
        text_rect = text_surface.get_rect()
        text_rect.left = self.display.get_rect().centerx + 10
        text_rect.centery = self.display.get_rect().centery - 100
        self.display.blit(text_surface, text_rect)

        text_surface = resources.get("basicFont").render('Register controllers by pressing start', True, (100, 100, 100))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.display.get_rect().centerx
        text_rect.centery = self.display.get_rect().centery +50
        self.display.blit(text_surface, text_rect)

        if self.player_controllers[0] is None:
            text = "P1 open"
        else:
            text = ""
        text_surface = resources.get("basicFont").render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.right = self.display.get_rect().centerx -  10
        text_rect.centery = self.display.get_rect().centery + 100
        self.display.blit(text_surface, text_rect)

        if self.player_controllers[1] is None:
            text = "P2 open"
        else:
            text = ""
        text_surface = resources.get("basicFont").render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.left = self.display.get_rect().centerx +  10
        text_rect.centery = self.display.get_rect().centery + 100
        self.display.blit(text_surface, text_rect)