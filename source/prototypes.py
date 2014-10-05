from components import *
import pygame

entities = None


def create_unit(position):
    unit = entities.create_entity()
    entities.add_component(unit, Position(position[0], position[1]))
    entities.add_component(unit, Velocity(0, 0))
    entities.add_component(unit, Groundable())
    entities.add_component(unit, Gravity())
    return unit


def create_player(position, type):
    player = create_unit(position)
    if type == "nyancat":
        image = resources.get("imgNyancat")
        entities.add_component(player, Collision(circle((0, 0), 50)))
        entities.add_component(player, Hurtvolume(rect((0, 0), 65, 55)))
        config = dict()
        config["hitshape"] = rect([40, 0], 50, 30)
        config["hitdamage"] = 10
        config["hitstun"] = 0.2
        config["hittime"] = 0.05
        config["speedMult"] = 1.6
        entities.add_component(player, Actor(config))
    elif type == "foreveralone":
        image = resources.get("imgForeverAlone")
        entities.add_component(player, Collision(circle((0, -10), 70)))
        entities.add_component(player, Hurtvolume(circle((0, -10), 70)))
        config = dict()
        config["hitshape"] = circle([60, 0], 40)
        config["hitdamage"] = 50
        config["hitstun"] = 0.4
        config["hittime"] = 0.2
        config["speedMult"] = 1.0
        entities.add_component(player, Actor(config))
    entities.add_component(player, Drawable(image))
    return player


def create_terrain(position, shape, image):
    terrain = entities.create_entity()
    entities.add_component(terrain, Position(position[0], position[1]))
    entities.add_component(terrain, Collision(shape))
    entities.add_component(terrain, Drawable(image))
    entities.add_component(terrain, Immovable())
    return terrain

def create_hitvolume(player):
    hitvol = entities.create_entity()
    actor = entities.component_for_entity(player, Actor)
    position = entities.component_for_entity(player, Position)
    hitshape = dict()
    hitshape["type"] = actor.config["hitshape"]["type"]
    hitshape["center"] = [actor.config["hitshape"]["center"][0], actor.config["hitshape"]["center"][1]]
    if hitshape["type"] == "rect":
        hitshape["width"] = actor.config["hitshape"]["width"]
        hitshape["height"] = actor.config["hitshape"]["height"]
    elif hitshape["type"] == "circle":
        hitshape["radius"] = actor.config["hitshape"]["radius"]
    entities.add_component(hitvol, Hitvolume(player, hitshape, actor.config["hitdamage"], actor.config["hitstun"]))
    entities.add_component(hitvol, Position(position.x, position.y))
    resources.get("logfile").write("{}, {}, {}\n".format(actor.config["hitshape"], position.x, position.y))