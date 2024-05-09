import pygame, sys
from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Rudra Man")
        
        #game clock
        self.clock = pygame.time.Clock()
        
        #create dictionary to pygame load files... give the path using join so that it works in every os
        self.tmx_maps  = {0: load_pygame(join("..", "data", "levels", "omni.tmx"))}
        
        #create levels and send map to the level
        self.current_stage = Level(self.tmx_maps[0])
        
    # the main run method    
    def run(self):
        while True:
            #data_time 
            dt= self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt)
            pygame.display.update()

            
if __name__ == "__main__":
    game = Game()
    game.run()