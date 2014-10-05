from ecs.models import System
from components import *
import pygame
import math

class DrawingSystem(System):
    def __init__(self, display):
        super(DrawingSystem, self).__init__()
        self.display = display
        self.display_rect = self.display.get_rect()

    def update(self, dt):
        self.display.fill((0, 50, 100))
        for entity, drawable in self.entity_manager.pairs_for_type(Drawable):
            position = self.entity_manager.component_for_entity(entity, Position)
            image = drawable.image
            if drawable.mirrored:
                image = pygame.transform.flip(image, True, False)
            self.display.blit(image, self.screen_position(position, drawable.image))

        for entity, actor in self.entity_manager.pairs_for_type(Actor):
            if actor.shielded > 0:
                position = self.entity_manager.component_for_entity(entity, Position)
                drawable = self.entity_manager.component_for_entity(entity, Drawable)
                image = drawable.image
                pygame.draw.circle(self.display, (0, 0, 255), self.screen_position(position, image), math.sqrt(image.get_with()*image.get_with() +image.get_height()*image.get_height())/2, 6)
                self.display.blit(image, self.screen_position(position, drawable.image))

    def screen_position(self, position, image):
        return (self.display_rect.centerx + position.x - image.get_width()/2, self.display_rect.centery + position.y - image.get_height()/2)


class DebugDrawingSystem(System):
    def __init__(self, display):
        super(DebugDrawingSystem, self).__init__()
        self.display = display
        self.display_rect = self.display.get_rect()

    def update(self, dt):
        collision_color = pygame.Color(100, 100, 100)
        for entity, collision in self.entity_manager.pairs_for_type(Collision):
            for shape in collision.shapes:
                position = self.entity_manager.component_for_entity(entity, Position)
                x = position.x + shape["center"][0]
                y = position.y + shape["center"][1]
                if shape["type"] == "circle":
                    pass#pygame.draw.circle(self.display, collision_color, self.screen_position((x, y)), shape["radius"], 0)
                elif shape["type"] == "rect":
                    screen_position = self.screen_position((x, y))
                    rect = (screen_position[0] - shape["width"]/2,
                            screen_position[1] - shape["height"]/2,
                            shape["width"], shape["height"])
                    #pygame.draw.rect(self.display, collision_color, rect, 0)

        for entity, hurtvol in self.entity_manager.pairs_for_type(Hurtvolume):
            position = self.entity_manager.component_for_entity(entity, Position)
            x = position.x + hurtvol.shape["center"][0]
            y = position.y + hurtvol.shape["center"][1]
            if hurtvol.shape["type"] == "circle":
                pygame.draw.circle(self.display, (255, 255, 0), self.screen_position((x, y)), hurtvol.shape["radius"], 0)
            elif hurtvol.shape["type"] == "rect":
                screen_position = self.screen_position((x, y))
                rect = (screen_position[0] - hurtvol.shape["width"]/2,
                        screen_position[1] - hurtvol.shape["height"]/2,
                        hurtvol.shape["width"], hurtvol.shape["height"])
                pygame.draw.rect(self.display, (255, 255, 0), rect, 0)

        for entity, hitvol in self.entity_manager.pairs_for_type(Hitvolume):
            position = self.entity_manager.component_for_entity(entity, Position)
            x = position.x + hitvol.shape["center"][0]
            y = position.y + hitvol.shape["center"][1]
            if hitvol.shape["type"] == "circle":
                pygame.draw.circle(self.display, (0, 255, 0), self.screen_position((x, y)), hitvol.shape["radius"], 0)
            elif hitvol.shape["type"] == "rect":
                screen_position = self.screen_position((x, y))
                rect = (screen_position[0] - hitvol.shape["width"]/2,
                        screen_position[1] - hitvol.shape["height"]/2,
                        hitvol.shape["width"], hitvol.shape["height"])
                pygame.draw.rect(self.display, (0, 255, 0), rect, 0)

        for entity, actor in self.entity_manager.pairs_for_type(Actor):
            position = self.entity_manager.component_for_entity(entity, Position)
            x = position.x + actor.config["hitshape"]["center"][0]
            y = position.y + actor.config["hitshape"]["center"][1]
            if actor.config["hitshape"]["type"] == "circle":
                pygame.draw.circle(self.display, (255, 0, 0), self.screen_position((x, y)), actor.config["hitshape"]["radius"], 0)
            elif actor.config["hitshape"]["type"] == "rect":
                screen_position = self.screen_position((x, y))
                rect = (screen_position[0] - actor.config["hitshape"]["width"]/2,
                        screen_position[1] - actor.config["hitshape"]["height"]/2,
                        actor.config["hitshape"]["width"], actor.config["hitshape"]["height"])
                pygame.draw.rect(self.display, (255, 0, 0), rect, 0)

    def screen_position(self, position):
        return (int(self.display_rect.centerx + position[0]), int(self.display_rect.centery + position[1]))