from components import *
from ecs.models import System
from utils import *
import math
import resources
import prototypes

class LinearMotionSystem(System):
    def __init__(self):
        super(LinearMotionSystem, self).__init__()

    def update(self, dt):
        for entity, velocity in self.entity_manager.pairs_for_type(Velocity):
            position = self.entity_manager.component_for_entity(entity, Position)
            position.x += velocity.dx * dt
            position.y += velocity.dy * dt
            #speed = length((velocity.dx, velocity.dy))
            velocity.dx -= resources.get("slowFactor") * velocity.dx
            velocity.dy -= resources.get("slowFactor") * velocity.dy


class GravitySystem(System):
    def __init__(self):
        super(GravitySystem, self).__init__()

    def update(self, dt):
        for entity, gravity in self.entity_manager.pairs_for_type(Gravity):
            velocity = self.entity_manager.component_for_entity(entity, Velocity)
            velocity.dy += gravity.g_factor * dt


class GroundingSystem(System):
    def __init__(self):
        super(GroundingSystem, self).__init__()

    def update(self, dt):
        for entity, groundable in self.entity_manager.pairs_for_type(Groundable):
            groundable.grounded = False


class CollisionSystem(System):
    def __init__(self):
        super(CollisionSystem, self).__init__()

    def update(self, dt):
        for entity, collision in self.entity_manager.pairs_for_type(Collision):
            position = self.entity_manager.component_for_entity(entity, Position)
            for entity2, collision2 in self.entity_manager.pairs_for_type(Collision):
                if entity == entity2 or entity > entity2:
                    continue
                position2 = self.entity_manager.component_for_entity(entity2, Position)
                found = False
                for shape in collision.shapes:
                    for shape2 in collision2.shapes:
                        result = collide_shapes((position, shape), (position2, shape2))
                        if result["occured"]:
                            found = True
                            break
                    if found:
                        break
                if found:
                    immovable = self.entity_manager.component_for_entity(entity, Immovable)
                    immovable2 = self.entity_manager.component_for_entity(entity2, Immovable)
                    if immovable is None and immovable2 is not None:
                        position.x += result["direction"][0]*result["depth"]
                        position.y += result["direction"][1]*result["depth"]
                        velocity = self.entity_manager.component_for_entity(entity, Velocity)
                        projection = dot((velocity.dx, velocity.dy), result["direction"])
                        if projection > 0:
                            velocity.dx -= 0.5*result["direction"][0]*projection
                            velocity.dy -= 0.5*result["direction"][1]*projection
                        else:
                            velocity.dx -= 1.1*result["direction"][0]*projection
                            velocity.dy -= 1.1*result["direction"][1]*projection
                        groundable = self.entity_manager.component_for_entity(entity, Groundable)
                        if groundable is not None:
                            groundable.grounded = True
                    elif immovable2 is None and immovable is not None:
                        position2.x -= result["direction"][0]*result["depth"]
                        position2.y -= result["direction"][1]*result["depth"]
                        velocity2 = self.entity_manager.component_for_entity(entity2, Velocity)
                        projection2 = dot((velocity2.dx, velocity2.dy), result["direction"])

                        if projection2 > 0:
                            projection2 = 0
                        velocity2.dx -= 1.7*result["direction"][0]*projection2
                        velocity2.dy -= 1.7*result["direction"][1]*projection2
                        groundable2 = self.entity_manager.component_for_entity(entity2, Groundable)
                        if groundable2 is not None:
                            groundable2.grounded = True
                    elif immovable is None and immovable2 is None:
                        pass
                        # position.x += result["direction"][0]*result["depth"]/2
                        # position.y += result["direction"][1]*result["depth"]/2
                        # position2.x -= result["direction"][0]*result["depth"]/2
                        # position2.y -= result["direction"][1]*result["depth"]/2
                        # velocity = self.entity_manager.component_for_entity(entity, Velocity)
                        # velocity2 = self.entity_manager.component_for_entity(entity, Velocity)
                        # projection = dot((velocity.dx, velocity.dy), result["direction"])
                        # projection2 = dot((velocity2.dx, velocity2.dy), result["direction"])
                        # if projection > 0:
                        #     velocity.dx += result["direction"][0]*projection
                        #     velocity.dy += result["direction"][1]*projection
                        #     groundable = self.entity_manager.component_for_entity(entity, Groundable)
                        #     if groundable is not None:
                        #         groundable.grounded = True
                        # if projection2 < 0:
                        #     velocity2.dx -= result["direction"][0]*projection2
                        #     velocity2.dy -= result["direction"][1]*projection2
                        #     groundable2 = self.entity_manager.component_for_entity(entity2, Groundable)
                        #     if groundable2 is not None:
                        #         groundable2.grounded = True

class ActorSystem(System):
    def __init__(self):
        super(ActorSystem, self).__init__()

    @staticmethod
    def direction_to_vec(dir):
        if dir == "neutral":
            return (0, 0)
        elif dir == "right":
            return (1, 0)
        elif dir == "left":
            return (-1, 0)
        elif dir == "up":
            return (0, -1)
        elif dir == "down":
            return (0, 1)

    def update(self, dt):
        for entity, actor in self.entity_manager.pairs_for_type(Actor):
            actor_velocity = self.entity_manager.component_for_entity(entity, Velocity)
            grounded = self.entity_manager.component_for_entity(entity, Groundable)
            if actor.acting > 0:
                actor.acting -= dt
                if actor.acting < 0:
                    actor.acting = 0

            if actor.stunned > 0:
                actor.stunned -= dt
                if actor.stunned < 0:
                    actor.stunned = 0

            if actor.shielded > 0:
                actor.shielded -= dt
                if actor.shielded < 0:
                    actor.shielded = 0

            velocity_change = (0, 0)
            action_time = 0
            for command in actor.commands:
                if actor.acting > 0 or actor.stunned > 0:
                    continue
                if command == "jump":
                    velocity_change = (0, -resources.get("jumpSpeed")*actor.config["speedMult"])
                    action_time = resources.get("normalTime")
                elif command == "shield":
                    actor.shielded = resources.get("shieldDuration")
                    action_time = resources.get("shieldTime")
                elif command == "attack":
                    prototypes.create_hitvolume(entity)
                    action_time = actor.config["hittime"]
            actor.acting += action_time
            actor_velocity.dx += velocity_change[0]
            actor_velocity.dy += velocity_change[1]
            actor.commands = []

            if grounded.grounded:
                actor.air_actions = resources.get("airActions")

            if actor.acting == 0 and actor.stunned == 0:
                if actor.orientation != actor.direction and actor.direction == "left" or actor.direction == "right":
                    if grounded.grounded:
                        actor_velocity.dx = actor_velocity.dx * resources.get("turnFactor")
                    actor.orientation = actor.direction
                    drawable = self.entity_manager.component_for_entity(entity, Drawable)
                    if actor.orientation == "left":
                        if actor.config["hitshape"]["center"][0] > 0:
                            actor.config["hitshape"]["center"][0] *= -1
                        drawable.mirrored = True
                    else:
                        if actor.config["hitshape"]["center"][0] < 0:
                            actor.config["hitshape"]["center"][0] *= -1
                        drawable.mirrored = False

            if actor.acting == 0 and actor.stunned == 0 and (grounded.grounded or actor.air_actions > 0):

                direction = ActorSystem.direction_to_vec(actor.direction)

                if actor.direction == "left" or actor.direction == "right":
                    velocity_change = mul(direction, resources.get("normalSpeed")*actor.config["speedMult"])
                    action_time = resources.get("normalTime")
                elif actor.direction == "up":
                    actor.commands.append("jump")
                elif actor.direction == "down":
                    if grounded.grounded:
                        velocity_change = (actor_velocity.dx, actor_velocity.dy)
                    else:
                        if math.fabs(actor_velocity.dy) < 20:
                            velocity_change = (0, -resources.get("jumpSpeed")*actor.config["speedMult"])
                        else:
                            velocity_change = (0, -0.5*resources.get("jumpSpeed")*actor.config["speedMult"])
                    if actor.impact:
                        velocity_change = mul(velocity_change, -1)
                    else:
                        velocity_change = mul(velocity_change, -0.66)
                    action_time = resources.get("normalTime")
                if not grounded.grounded:
                        actor.air_actions -= 1
                if actor.impact:
                    action_time *= resources.get("impactTimeFactor")
            actor.acting += action_time
            actor_velocity.dx += velocity_change[0]
            actor_velocity.dy += velocity_change[1]


class DamageSystem(System):
    def __init__(self):
        super(DamageSystem, self).__init__()

    def update(self, dt):
        for entity, hurtvolume in self.entity_manager.pairs_for_type(Hurtvolume):
            hurtpos = self.entity_manager.component_for_entity(entity, Position)
            for entity2, hitvolume in self.entity_manager.pairs_for_type(Hitvolume):
                if entity == hitvolume.player or not hitvolume.active:
                    continue
                hitpos = self.entity_manager.component_for_entity(entity2, Position)
                collision = collide_shapes((hurtpos, hurtvolume.shape), (hitpos, hitvolume.shape))
                if collision["occured"]:
                    actor = self.entity_manager.component_for_entity(entity, Actor)
                    if actor.shielded:
                        continue
                    else:
                        actor.stunned = hitvolume.stun
                        actor.damage += hitvolume.damage
                        hitaccel = mul(collision["direction"], hitvolume.damage * actor.damage * resources.get("hitFactor"))
                        actor_velocity = self.entity_manager.component_for_entity(entity, Velocity)
                        actor_velocity.dx += hitaccel[0]
                        actor_velocity.dy += hitaccel[1]

        volumes = []
        for entity, hitvolume in self.entity_manager.pairs_for_type(Hitvolume):
            hitvolume.active = False
            volumes.append(entity)

        for ent in volumes:
            pass#self.entity_manager.remove_entity(ent)





def collide_shapes(collider, collider2):
    collision = dict()
    collision["occured"] = False
    collision["direction"] = None
    collision["depth"] = None
    position = collider[0]
    position2 = collider2[0]
    collision_shape = collider[1]
    collision_shape2 = collider2[1]
    delta_x = (position2.x + collision_shape2["center"][0]) - (position.x + collision_shape["center"][0])
    delta_y = (position2.y + collision_shape2["center"][1]) - (position.y + collision_shape["center"][1])
    if collision_shape["type"] == "circle" and collision_shape2["type"] == "circle":
        summed_radii = collision_shape["radius"] + collision_shape2["radius"]
        if length_sq((delta_x, delta_y)) < summed_radii*summed_radii:
            collision["occured"] = True
            collision["direction"] = normalized((-delta_x, -delta_y))
            collision["depth"] = summed_radii - length((delta_x, delta_y))
    elif collision_shape["type"] == "rect" and collision_shape2["type"] == "rect":
        ranges = (collision_shape["width"]/2+collision_shape2["width"]/2, collision_shape["height"]/2+collision_shape2["height"]/2)
        if math.fabs(delta_x) < ranges[0] and math.fabs(delta_y) < ranges[1]:
            if math.fabs(math.fabs(delta_x)- ranges[0]) < math.fabs(math.fabs(delta_y)- ranges[1]):
                collision["occured"] = True
                collision["direction"] = (-math.copysign(1, delta_x), 0)
                collision["depth"] = ranges[0] - math.fabs(delta_x)
            else:
                collision["occured"] = True
                collision["direction"] = (0, -math.copysign(1, delta_y))
                collision["depth"] = ranges[1] - math.fabs(delta_y)
    else:
        circle = None
        rect = None
        if collision_shape["type"] == "rect" and collision_shape2["type"] == "circle":
            rect = collision_shape
            circle = collision_shape2
        elif collision_shape["type"] == "circle" and collision_shape2["type"] == "rect":
            circle = collision_shape
            rect = collision_shape2
        distance_to_rect = (math.fabs(delta_x) - rect["width"]/2, math.fabs(delta_y) - rect["height"]/2)
        if distance_to_rect[0] < 0 and distance_to_rect[1] < 0:
            collision["occured"] = True
            if distance_to_rect[0] < distance_to_rect[1]:
                collision["direction"] = (-math.copysign(1, delta_x), 0)
            else:
                collision["direction"] = (0, -math.copysign(1, delta_y))
            collision["depth"] = length(distance_to_rect)+ circle["radius"]
        elif distance_to_rect[0] < 0 and distance_to_rect[1] >= 0 and distance_to_rect[1] < circle["radius"]:
            collision["occured"] = True
            collision["direction"] = (0, -math.copysign(1, delta_y))
            collision["depth"] = circle["radius"] - distance_to_rect[1]
        elif distance_to_rect[1] < 0 and distance_to_rect[0] >= 0 and distance_to_rect[0] < circle["radius"]:
            collision["occured"] = True
            collision["direction"] = (-math.copysign(1, delta_x), 0)
            collision["depth"] = circle["radius"] - distance_to_rect[0]
        elif length_sq(distance_to_rect) < circle["radius"]*circle["radius"]:
            collision["occured"] = True
            collision["direction"] = normalized((-math.copysign(1, delta_x)*distance_to_rect[0], -math.copysign(1, delta_y)*distance_to_rect[1]))
            collision["depth"] = circle["radius"] - length(distance_to_rect)
    return collision