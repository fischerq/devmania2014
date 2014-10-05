from ecs.models import Component
import resources

class Position(Component):
    def __init__(self, x, y):
        super(Position, self).__init__()
        self.x = x
        self.y = y


class Velocity(Component):
    def __init__(self, dx, dy):
        super(Velocity, self).__init__()
        self.dx = dx
        self.dy = dy


class Gravity(Component):
    def __init__(self):
        super(Gravity, self).__init__()
        self.g_factor = resources.get("gravity")


class Collision(Component):
    def __init__(self, shape):
        super(Collision, self).__init__()
        self.shapes = [shape]

    def add_shape(self, shape):
        self.shapes.append(shape)


class Immovable(Component):
    def __init__(self):
        super(Immovable, self).__init__()


class Groundable(Component):
    def __init__(self):
        super(Groundable, self).__init__()
        self.grounded = False


class Actor(Component):
    def __init__(self):
        super(Actor, self).__init__()
        self.direction = "neutral"
        self.orientation = "right"
        self.impact = None
        self.acting = 0
        self.stunned = 0
        self.shielded = 0
        self.air_actions = resources.get("airActions")
        self.commands = []
        self.damage = 0



class Drawable(Component):
    def __init__(self, image):
        super(Drawable, self).__init__()
        self.image = image
        self.visible = True
        self.mirrored = False


class Hitvolume(Component):
    def __init__(self, player, shape, damage):
        super(Hitvolume, self).__init__()
        self.player = player
        self.shape = shape
        self.damage = damage

class Hurtvolume(Component):
    def __init__(self, player, shape, damage):
        super(Hurtvolume, self).__init__()
        self.shape = shape

def circle(center, radius):
    shape = dict()
    shape["type"] = "circle"
    shape["center"] = center
    shape["radius"] = radius
    return shape


def rect(center, width, height):
    shape = dict()
    shape["type"] = "rect"
    shape["center"] = center
    shape["width"] = width
    shape["height"] = height
    return shape