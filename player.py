from settings import *
from pygame.sprite import Group

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48,56))
        self.image.fill("red")
        
        #rects
        self.rect = self.image.get_frect(topleft = pos)
        #this is to check from which direction the rect is coming from to check for the collision. so it stores the previous position 
        self.old_rect = self.rect.copy()
        
        #player movements variables
        self.direction = vector()
        self.speed = 300
        self.gravity = 1300 
        
        #collision
        self.collision_sprites = collision_sprites
        print(self.collision_sprites)
      
    #key inputs  
    def input(self):
        keys= pygame.key.get_pressed()
        # no movements until key is pressed
        input_vector = vector(0,0)
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x #using normalise prevents from the speeding from increasing
    
    #player movements based on inputs
    def move(self, dt):
        #horizontal movements
        self.rect.x += self.direction.x * self.speed * dt
        #check for collision in x axis
        self.collision("horizontal")
        
        #virtical movements
        self.direction.y += self.gravity / 2 * dt #for the accelaration of gravty
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt #for the accelaration of gravty
        #check for virtical movements
        self.collision("virtical")
        
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                #horizontal collisions
                if axis == "horizontal":
                    #left side collision check
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    #right side collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        
                
                if axis == "virtical":
                    #top collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        
                    #bottom collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    
                    #if collision is found virtically then gravity shouldn't work
                    self.direction.y = 0
    
    #run all methods in this method
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)