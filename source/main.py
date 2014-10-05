import pygame, sys
from pygame.locals import *
from application import Application
import resources

title = "SuperMemeBros"
clearColor = pygame.Color(255, 255, 255)


def main():
    # set up pygame
    pygame.init()
    # set up the window
    window_surface = pygame.display.set_mode((1024, 768), pygame.DOUBLEBUF | pygame.HWSURFACE) #pygame.FULLSCREEN
    pygame.display.set_caption(title)
    fps_clock = pygame.time.Clock()
    joysticks = []
    for i in range(0, pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
            joysticks[-1].init()
    resources.set("joysticks", joysticks)
    app = Application(window_surface)
    resources.load()
    window_active = True
    # run the game loop
    while True:
        #read input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ACTIVEEVENT:
                if event.state == 2:
                    window_active = False
                elif event.state == 1:
                    window_active = True
                elif event.state == 6:
                    window_active = False
                #print event
            else:
                if window_active:
                    app.input(event)
        if window_active:
            app.update()
            window_surface.fill(clearColor)
            app.render()
            pygame.display.update()
        fps_clock.tick(resources.get("fps"))


if __name__ == '__main__':
    main()