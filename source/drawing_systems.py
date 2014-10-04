from ecs.models import System
from components import *
import pygame


class DrawingSystem(System):
    def __init__(self, display):
        super(DrawingSystem, self).__init__()
        self.display = display
        self.display_rect = self.display.get_rect()

    def update(self, dt):
        for entity, drawable in self.entity_manager.pairs_for_type(Drawable):
            position = self.entity_manager.component_for_entity(entity, Position)
            self.display.blit(drawable.image, self.screen_position(position, drawable.image))

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
            position = self.entity_manager.component_for_entity(entity, Position)
            x = position.x + collision.shape["center"][0]
            y = position.y + collision.shape["center"][1]
            if collision.shape["type"] == "circle":
                pygame.draw.circle(self.display, collision_color, self.screen_position((x, y)), collision.shape["radius"], 0)
            elif collision.shape["type"] == "rect":
                screen_position = self.screen_position((x, y))
                rect = (screen_position[0] - collision.shape["width"]/2,
                        screen_position[1] - collision.shape["height"]/2,
                        collision.shape["width"], collision.shape["height"])
                pygame.draw.rect(self.display, collision_color, rect, 0)

        for entity, debug_drawable in self.entity_manager.pairs_for_type(DebugDrawable):
            position = self.entity_manager.component_for_entity(entity, Position)
            if debug_drawable.shape["type"] == "circle":
                pygame.draw.circle(self.display, debug_drawable.color, self.screen_position((position.x, position.y)), debug_drawable.shape["radius"], 0)
            elif debug_drawable.shape["type"] == "rect":
                screen_position = self.screen_position((position.x, position.y))
                rect = (screen_position[0] - debug_drawable.shape["width"]/2,
                        screen_position[1] - debug_drawable.shape["height"]/2,
                        debug_drawable.shape["width"], debug_drawable.shape["height"])
                pygame.draw.rect(self.display, debug_drawable.color, rect, 0)

    def screen_position(self, position):
        return (int(self.display_rect.centerx + position[0]), int(self.display_rect.centery + position[1]))