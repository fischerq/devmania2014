import math

def length(vector):
    return math.sqrt(length_sq(vector))


def length_sq(vector):
    return vector[0]*vector[0] + vector[1]*vector[1]


def normalized(vector):
    length = math.sqrt(length_sq(vector))
    return (vector[0]/length, vector[1]/length)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(vec, fac):
    return (vec[0]*fac, vec[1]*fac)


def dot(a, b):
    if a is None:
        print "a"
    elif b is None:
        print "b"
    return a[0]*b[0]+a[1]*b[1]

def map_buttons(button):
    if button == 0:
        return "X"
    elif button == 1:
        return "A"
    elif button == 2:
        return "B"
    elif button == 3:
        return "Y"
    elif button == 4:
        return "L"
    elif button == 5:
        return "R"
    elif button == 7:
        return "Z"

def map_axis(axis):
    if axis == 0:
        return "stick"
    elif axis == 1:
        return "stick"
    elif axis == 2:
        return "cstick"
    elif axis == 3:
        return "cstick"
    elif axis == 4:
        return "R"
    elif axis == 5:
        return "L"