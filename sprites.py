from pygame.sprite import Group
from settings import *


#createing a sprite class and that inherits a Sprite class from pygame
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE,TILE_SIZE)), groups = None):
        super().__init__(groups)
        self.image = surf
        self.image.fill("white")
        
        #rect
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        
class MovingSprites(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_dir, speed):
        surf = pygame.Surface((200, 50))
        super().__init__(start_pos, surf, groups)
        self.rect.center = start_pos