from components import *
import pygame

entities = None


def create_unit(position):
    unit = entities.create_entity()
    entities.add_component(unit, Position(position[0], position[1]))
    entities.add_component(unit, Velocity(0, 0))
    entities.add_component(unit, Groundable())
    entities.add_component(unit, Gravity())
    entities.add_component(unit, Actor())
    return unit


def create_player(position, type):
    player = create_unit(position)
    if type == "nyancat":
        image = resources.get("imgNyancat")
        entities.add_component(player, Collision(rect((0, 0), 65, 55)))
        entities.add_component(player, Hurtvolume(rect((0, 0), 65, 55)))
    elif type == "foreveralone":
        image = resources.get("imgForeverAlone")
        entities.add_component(player, Collision(rect((0, 30), 40, 20)))
        collision = entities.component_for_entity(player, Collision)
        collision.add_shape(circle((0, -10), 70))
        entities.add_component(player, Hurtvolume(rect((0, 30), 40, 20)))
    entities.add_component(player, Drawable(image))


    return player


def create_terrain(position, rectangle, image):
    terrain = entities.create_entity()
    entities.add_component(terrain, Position(position[0], position[1]))
    entities.add_component(terrain, Collision(rect((0, 0), rectangle[0], rectangle[1])))
    entities.add_component(terrain, Drawable(image))
    entities.add_component(terrain, Immovable())
    return terrain