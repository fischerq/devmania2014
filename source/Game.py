import resources
from pygame.locals import *
from systems import *
from drawing_systems import *
from components import *
from ecs.managers import EntityManager, SystemManager
import prototypes
import utils

class Game:
    def __init__(self, display):
        self.display = display
        self.offset = 0
        self.entities = EntityManager()
        prototypes.entities = self.entities
        self.systems = SystemManager(self.entities)
        self.systems.add_system(LinearMotionSystem())
        self.systems.add_system(GravitySystem())
        self.systems.add_system(GroundingSystem())
        self.systems.add_system(CollisionSystem())
        self.systems.add_system(ActorSystem())
        self.drawing_systems = SystemManager(self.entities)
        self.drawing_systems.add_system(DrawingSystem(self.display))
        self.drawing_systems.add_system(DebugDrawingSystem(self.display))
        self.players = (None, None)
        self.lives = [5, 5]
        self.winner = None
        self.player_controllers = resources.get("player_joysticks")
        self.old_sticks = []
        self.joysticks = [resources.get("joysticks")[self.player_controllers[0]], resources.get("joysticks")[self.player_controllers[1]]]
        self.maxmin = [0, 0, 0, 0]
        self.logfile = resources.get("logfile")
        self.create_world()

    def create_world(self):
        p1 = prototypes.create_player((-100, 0), "foreveralone")
        p2 = prototypes.create_player((100, 0), "nyancat")
        self.players = (p1, p2)
        terrain = prototypes.create_terrain((0, 200), (750, 60), resources.get("imgTerrain"))

    def process_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return "exit"

        elif event.type == JOYAXISMOTION:
            pass
            #print "Joystick '",event.joy,"' axis",event.axis,"motion."
            #player = None
            #if event.joy == self.player_controllers[0]:
            #    player = 0
            #elif event.joy == self.player_controllers[1]:
            #    player = 1
            #if utils.map_axis(event.axis) == "stick":
            #    return (player, utils.map_axis(event.axis))
        elif event.type == JOYBUTTONDOWN:
            player = None
            if event.joy == self.player_controllers[0]:
                player = 0
            elif event.joy == self.player_controllers[1]:
                player = 1
            return (player, utils.map_buttons(event.button))
        elif event.type == JOYBUTTONUP:
                print "Joystick '",event.joy,"' button",event.button,"up."
        elif event.type == JOYHATMOTION:#disabled
                pass# print "Joystick '",event.joy,"' hat",event.hat," moved.", event.value
        return None

    def add_command(self, player, command):
        actor = self.entities.component_for_entity(self.players[player], Actor)
        actor.commands.append(command)

    def update(self, commands):
        #self.logfile.write("frame\n")
        impact = [False, False]
        direction = [None, None]

        stick_0 = self.evaluate_joystick(0)
        stick_1 = self.evaluate_joystick(1)
        if self.old_sticks != []:
            change1 = length(sub(self.old_sticks[0]["stick"], stick_0["stick"]))
            if change1 > resources.get("impactThreshold"):
                impact[0] = True
            #self.logfile.write("p1 {}\n".format(stick_0["stick"]))
            position = length(stick_0["stick"])
            if position < 0.1:
                direction[0] = "neutral"
            else:
                stickdir = utils.normalized(stick_0["stick"])
                if stickdir[0] > 0.7:
                    direction[0] = "right"
                elif stickdir[0] < -0.7:
                    direction[0] = "left"
                elif stickdir[1] > 0.7:
                    direction[0] = "down"
                elif stickdir[1] < -0.7:
                    direction[0] = "up"

            #self.logfile.write("p1 dir {}\n".format(direction[0]))

            change2 = length(sub(self.old_sticks[1]["stick"], stick_1["stick"]))
            if change2 > resources.get("impactThreshold"):
                impact[1] = True
            position = length(stick_1["stick"])
            if position < 0.1:
                direction[1] = "neutral"
            else:
                stickdir = utils.normalized(stick_1["stick"])
                if stickdir[0] > 0.7:
                    direction[1] = "right"
                elif stickdir[0] < -0.7:
                    direction[1] = "left"
                elif stickdir[1] > 0.7:
                    direction[1] = "down"
                elif stickdir[1] < -0.7:
                    direction[1] = "up"

            #self.logfile.write("p2 dir {}\n".format(direction[1]))

            actor = self.entities.component_for_entity(self.players[0], Actor)
            actor.direction = direction[0]
            actor.impact = impact[0]

            actor = self.entities.component_for_entity(self.players[1], Actor)
            actor.direction = direction[1]
            actor.impact = impact[1]
        else:
            self.old_sticks = [None, None]

        self.old_sticks[0] = stick_0
        self.old_sticks[1] = stick_1

        for command in commands:
            if command == "exit":
                return "finish"
            if len(command) == 2:
                if command[1] == "A":
                    self.add_command(command[0], "attack")
                if command[1] == "L":
                    self.add_command(command[0], "shield")

        self.systems.update(1.0/resources.get("fps"))

        position = self.entities.component_for_entity(self.players[0], Position)
        if position.x < -512 or position.x > 512 or position.y < -284 or position.y > 400:
            self.lives[0] -= 1
            position.x = 0
            position.y = 0
            if self.lives[0] == 0:
                self.winner = 1
        position = self.entities.component_for_entity(self.players[1], Position)
        if position.x < -512 or position.x > 512 or position.y < -284 or position.y > 400:
            self.lives[1] -= 1
            position.x = 0
            position.y = 0
            if self.lives[1] == 0:
                self.winner = 0
        return None

    def evaluate_joystick(self, id):
        joystick = self.joysticks[self.player_controllers[id]]
        state = dict()
        state["stick"] = (joystick.get_axis(0), joystick.get_axis(1))
        #state["cstick"] = (0, 0)#(joystick.get_axis(2), joystick.get_axis(3))
        return state

    def render(self):
        if self.winner is None:
            self.drawing_systems.update(1)

            icon = resources.get("imgAloneIcon")
            position = (50, 500)
            for i in range(0, self.lives[0]):
                self.display.blit(icon, (position[0]+i*icon.get_width(), position[1]))

            icon = resources.get("imgNyancatIcon")
            position = (700, 500)
            for i in range(0, self.lives[0]):
                self.display.blit(icon, (position[0]+i*icon.get_width(), position[1]))

        else:
            self.display.blit(resources.get("imgBackgroundGO"), (0, 0))

            self.display.blit(resources.get("imgGOString"), (300, 150))

            if self.winner == 0:
                string = "Player1 wins!"
                color = (255, 0, 0)
            elif self.winner == 1:
                string = "Player2 wins!"
                color = (0, 0, 255)
            text_surface = resources.get("basicFont").render(string, True, color)
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.display.get_rect().centerx
            text_rect.centery = self.display.get_rect().centery
            self.display.blit(text_surface, text_rect)