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
        self.fsm.onchangestate = Application.change_state
        self.commands = []
        self.active_state = Menu(self.display)

    @staticmethod
    def change_state(event):
        app = event.app
        if event.dst == "menu":
            app.active_state = Menu(app.display)
        elif event.dst == "game":
            app.active_state = Game(app.display)
        elif event.dst == "credits":
            app.active_state = Credits(app.display)

    def input(self, event):
        command = self.active_state.process_input(event)
        if command != None:
            self.commands.append(command)

    def update(self):
        transition = self.active_state.update(self.commands)
        if transition is not None:
            self.fsm.trigger(transition, app=self)
        self.commands = []

    def render(self):
        self.active_state.render()