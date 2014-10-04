import pygame

resources = {}


def load():
    resources["basicFont"] = pygame.font.SysFont("Arial", 48)
    resources["fps"] = 60
    resources["imgForeverAlone"] = pygame.image.load("../data/img/forever_alone.png").convert_alpha()
    resources["imgTerrain"] = pygame.image.load("../data/img/terrain.png").convert_alpha()


def get(name):
    return resources[name]


