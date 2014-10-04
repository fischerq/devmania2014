import pygame

resources = {}

def load():
    resources["basicFont"] = pygame.font.SysFont("Arial", 48)

def get(name):
    return resources[name]


