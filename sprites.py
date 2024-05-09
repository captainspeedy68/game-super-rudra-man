from pygame.sprite import Group
from settings import *


#createing a sprite class and that inherits a Sprite class from pygame
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill("white")
        
        #rect
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()