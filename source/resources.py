import pygame

resources = {}


def load():
    resources["logfile"] = open("log.txt", "w+")
    resources["TitleFont"] = pygame.font.SysFont("Impact", 64)
    resources["basicFont"] = pygame.font.SysFont("Arial", 36)
    resources["fps"] = 60
    resources["imgForeverAlone"] = pygame.image.load("../data/img/forever_alone.png").convert_alpha()
    resources["imgNyancat"] = pygame.image.load("../data/img/nyancat_clean.png").convert_alpha()
    resources["imgTerrain"] = pygame.image.load("../data/img/terrain.png").convert_alpha()
    resources["imgTile"] = pygame.image.load("../data/img/regenbogen.png").convert_alpha()
    resources["imgCake"] = pygame.image.load("../data/img/cake1.png").convert_alpha()

    resources["imgNyancatIcon"] = pygame.transform.scale(pygame.image.load("../data/img/cat1.png").convert_alpha(), (49, 60))
    resources["imgAloneIcon"] = pygame.transform.scale(pygame.image.load("../data/img/lolly1.png").convert_alpha(), (49, 60))

    resources["imgBackgroundGO"] = pygame.image.load("../data/img/BG_GameOver.png").convert_alpha()
    resources["imgGOString"] = pygame.image.load("../data/img/GameOver.png").convert_alpha()

    resources["imgBackgroundMenu"] = pygame.image.load("../data/img/bg/bg1.png").convert_alpha()
    resources["imgMenuTitle"] = pygame.image.load("../data/img/title.png").convert_alpha()

    resources["slowFactor"] = 0.05
    resources["gravity"] = 500

    resources["normalSpeed"] = 250
    resources["normalTime"] = 0.25

    resources["impactFactor"] = 2
    resources["impactTimeFactor"] = 0.5

    resources["jumpSpeed"] = 300
    resources["airActions"] = 5

    resources["turnFactor"] = 0.9
    resources["impactThreshold"] = 0.2

    resources["hitFactor"] = 1

    resources["shieldDuration"] = 0.4
    resources["shieldTime"] = 0.5

def get(name):
    return resources[name]

def set(name, value):
    resources[name] = value


