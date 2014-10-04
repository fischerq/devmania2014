from components import *
import pygame

entities = None


def create_unit(position):
    unit = entities.create_entity()
    entities.add_component(unit, Position(position[0], position[1]))
    entities.add_component(unit, Velocity(0, 0))
    entities.add_component(unit, Gravity())
    entities.add_component(unit, DebugDrawable(pygame.Color(0, 0, 255), DebugDrawable.circle(16)))
    return unit


def create_terrain(position, rect, image):
    terrain = entities.create_entity()
    entities.add_component(terrain, Position(position[0], position[1]))
    entities.add_component(terrain, Collision.rect((0,0), rect[0], rect[1]))
    entities.add_component(terrain, DebugDrawable(pygame.Color(255, 255, 0), DebugDrawable.circle(16)))
    entities.add_component(terrain, Drawable(image))
    return terrain