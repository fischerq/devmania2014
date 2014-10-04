import pygame, sys
from pygame.locals import *
from application import Application
import resources

fps = 60
title = "Game" # TODO
clearColor = pygame.Color(255, 255, 255)

def main():
    # set up pygame
    pygame.init()
    # set up the window
    windowSurface = pygame.display.set_mode((1024, 568), pygame.DOUBLEBUF | pygame.HWSURFACE) #pygame.FULLSCREEN
    pygame.display.set_caption(title)
    fpsClock = pygame.time.Clock()
    app = Application(windowSurface)
    resources.load()
    windowActive = True
    # run the game loop
    while True:
        #read input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ACTIVEEVENT:
                if event.state == 2:
                    windowActive = False
                elif event.state == 1:
                    windowActive = True
                elif event.state == 6:
                    windowActive = False
                #print event
            else:
                if windowActive:
                    app.input(event)
        if windowActive:
            app.update()
            windowSurface.fill(clearColor)
            app.render()
            pygame.display.update()
        fpsClock.tick(fps)


if __name__ == '__main__':
    main()