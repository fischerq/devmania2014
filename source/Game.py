import resources
from pygame.locals import *
from systems import *
from drawing_systems import *
from components import *
from ecs.managers import EntityManager, SystemManager
import prototypes

class Game:
    def __init__(self, display):
        self.display = display
        self.offset = 0
        self.entities = EntityManager()
        prototypes.entities = self.entities
        self.systems = SystemManager(self.entities)
        self.systems.add_system(LinearMotionSystem())
        self.systems.add_system(GravitySystem())
        self.drawing_systems = SystemManager(self.entities)
        self.drawing_systems.add_system(DrawingSystem(self.display))
        self.drawing_systems.add_system(DebugDrawingSystem(self.display))
        self.create_world()

    def create_world(self):
        player = prototypes.create_unit((-100, 0))
        self.entities.add_component(player, Drawable(resources.get("imgForeverAlone")))
        debug = self.entities.component_for_entity(player, DebugDrawable)
        debug.color = pygame.Color(255, 0, 0)
        debug.shape = DebugDrawable.rect(30, 20)
        self.entities.add_component(player, Collision.circle((20, 20), 16))

        terrain = prototypes.create_terrain((0, 200), (350, 60), resources.get("imgTerrain"))

    def process_input(self, event):
        if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "exit"
        return None

    def update(self, commands):
        for command in commands:
            if command == "exit":
                return "finish"
        self.systems.update(1.0/resources.get("fps"))
        self.offset += 1
        if self.offset > self.display.get_rect().width/2:
           self.offset -= self.display.get_rect().width
        return None

    def render(self):
        self.drawing_systems.update(1)
        color = (0, 0, 0)
        textSurface = resources.get("basicFont").render('Game', True, color, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = self.display.get_rect().centerx
        textRect.centery = self.display.get_rect().centery
        self.display.blit(textSurface, textRect)