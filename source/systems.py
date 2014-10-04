from components import *
from ecs.models import System


class LinearMotionSystem(System):
    def __init__(self):
        super(LinearMotionSystem, self).__init__()

    def update(self, dt):
        for entity, velocity in self.entity_manager.pairs_for_type(Velocity):
            position = self.entity_manager.component_for_entity(entity, Position)
            position.x += velocity.dx * dt
            position.y += velocity.dy * dt


class GravitySystem(System):
    def __init__(self):
        super(GravitySystem, self).__init__()

    def update(self, dt):
        for entity, gravity in self.entity_manager.pairs_for_type(Gravity):
            velocity = self.entity_manager.component_for_entity(entity, Velocity)
            velocity.dy += gravity.g_factor * dt

