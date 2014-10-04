from ecs.models import Component


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
        self.g_factor = 30


class Collision(Component):
    def __init__(self, shape):
        super(Collision, self).__init__()
        self.shape = shape

    @staticmethod
    def circle(center, radius):
        shape = dict()
        shape["type"] = "circle"
        shape["center"] = center
        shape["radius"] = radius
        return Collision(shape)

    @staticmethod
    def rect(center, width, height):
        shape = dict()
        shape["type"] = "rect"
        shape["center"] = center
        shape["width"] = width
        shape["height"] = height
        return Collision(shape)



class Drawable(Component):
    def __init__(self, image):
        super(Drawable, self).__init__()
        self.image = image
        self.visible = True


class DebugDrawable(Component):
    def __init__(self, color, shape):
        super(DebugDrawable, self).__init__()
        self.color = color
        self.shape = shape

    @staticmethod
    def circle(radius):
        shape = dict()
        shape["type"] = "circle"
        shape["radius"] = radius
        return shape

    @staticmethod
    def rect(width, height):
        shape = dict()
        shape["type"] = "rect"
        shape["width"] = width
        shape["height"] = height
        return shape