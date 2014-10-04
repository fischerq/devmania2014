import pygame
from pygame.locals import *

from fysom import Fysom

class InputPrinter:
    def __init__(self):
        pass

    def process(self, event):
        if event.type == KEYDOWN:
                print "Keydown,",event.key
        elif event.type == KEYUP:
                print "Keyup,",event.key
        elif event.type == MOUSEMOTION:
#                print "Mouse movement detected."
            pass
        elif event.type == MOUSEBUTTONDOWN:
                print "Mouse button",event.button,"down at",pygame.mouse.get_pos()
        elif event.type == MOUSEBUTTONUP:
                print "Mouse button",event.button,"up at",pygame.mouse.get_pos()
        elif event.type == JOYAXISMOTION:
                print "Joystick '",event.joy,"' axis",event.axis,"motion."
        elif event.type == JOYBUTTONDOWN:
                print "Joystick '",event.joy,"' button",event.button,"down."
        elif event.type == JOYBUTTONUP:
                print "Joystick '",event.joy,"' button",event.button,"up."
        elif event.type == JOYHATMOTION:
                print "Joystick '",event.joy,"' hat",event.hat," moved.", event.value
        return None


