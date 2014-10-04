import pygame
import resources
from menu import Menu
from game import Game
from credits import Credits
from fysom import Fysom

class Application():
    def __init__(self, display):
        self.display = display
        self.offset = 0
        self.fsm = Fysom({ 'initial': 'menu',
            'events': [
                {'name': 'start', 'src': 'menu', 'dst': 'game'},
                {'name': 'finish', 'src': 'game', 'dst': 'menu'},
                {'name': 'credits', 'src': 'menu', 'dst': 'credits'},
                {'name': 'menu', 'src': 'credits', 'dst': 'menu'} ] })
        self.fsm.onchangestate = self.changeState
        self.commands = []
        self.activeState = Menu(self.display)

    def changeState(self, event):
        app = event.app
        if event.dst == "menu":
            app.activeState = Menu(app.display)
        elif event.dst == "game":
            app.activeState = Game(app.display)
        elif event.dst == "credits":
            app.activeState = Credits(app.display)

    def input(self, event):
        command = self.activeState.processInput(event)
        if command != None:
            self.commands.append(command)

    def update(self):
        transition = self.activeState.update(self.commands)
        if transition != None:
            self.fsm.trigger(transition, app=self)
        self.commands = []

    def render(self):
        self.activeState.render()