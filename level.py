from settings import *
from sprites import Sprite, MovingSprites
from player import Player
class Level:
    def __init__(self, tmx_map):
        # display surface of the level
        self.display_surface = pygame.display.get_surface()
        
        
        
        #groups
        #an instance of sprite class
        self.all_sprites = pygame.sprite.Group()
        self.collsion_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
        
        
    def setup(self, tmx_map):
        #tiles
        
        #call the component layer by name from maps and distructure properties to use in for loop
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            
            #creating instance of sprite class and pixelising the position
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, (self.all_sprites, self.collsion_sprites))
        
        #objects
        #getting the player object
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                Player((obj.x, obj.y), self.all_sprites, self.collsion_sprites)
                
                
        #moving objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "helicopter":
                if (obj.width > obj.height): #horizontal movement
                    move_dir = "x"
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: #virtical movement
                    move_dir = "y"
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties["speed"]
                MovingSprites(self.all_sprites, start_pos, end_pos, move_dir, speed)
                
    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill("gray")
        self.all_sprites.draw(self.display_surface)