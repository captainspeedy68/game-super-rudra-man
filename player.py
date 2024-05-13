from settings import *
from pygame.sprite import Group
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites):
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
        self.jump = False
        self.jump_height = -900
        
        #collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}
        
        #check for moving platforms
        self.platform = None    
        
        #timer
        self.timer = {
            "wall jump": Timer(400),
            "wall slide block": Timer(200)
        }
      
    #key inputs  
    def input(self):
        keys= pygame.key.get_pressed()
        # no movements until key is pressed
        input_vector = vector(0,0)
        if not self.timer["wall jump"].active:
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x #using normalise prevents from the speeding from increasing
            
        if keys[pygame.K_SPACE]:
            self.jump = True
            
    
    #player movements based on inputs
    def move(self, dt):
        #horizontal movements
        self.rect.x += self.direction.x * self.speed * dt
        #check for collision in x axis
        #wall slide
        self.collision("horizontal")
        if not self.on_surface["floor"] and any((self.on_surface["left"], self.on_surface["right"])) and not self.timer["wall slide block"].active:
            self.direction.y = 0

            # change the gravity style when hit the walls
            self.rect.y += self.gravity / 10 * dt
        else:
            #virtical movements
            self.direction.y += self.gravity / 2 * dt #for the accelaration of gravty
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt #for the accelaration of gravty
        #check for virtical movements
        self.collision("virtical")
        
        
        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = self.jump_height
                self.timer["wall slide block"].activate()
                self.rect.bottom -= 1
            elif any((self.on_surface["left"], self.on_surface["right"])) and not self.timer["wall slide block"].active:
                self.timer["wall jump"].activate()
                self.direction.y = self.jump_height
                # if self.on_surface["left"]:
                #     self.direction.x = 1
                # else: self.direction.x = -1
                self.direction.x = 1 if self.on_surface["left"] else -1
            self.jump = False
        
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
                        if hasattr(sprite, "moving"):
                            self.rect.top += 6
                        
                    #bottom collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    
                    #if collision is found virtically then gravity shouldn't work
                    self.direction.y = 0
                
    #to make sure that player is moving with the moving platform
    def platform_move(self, dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt
    
    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        
        right_side_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2))
        
        left_side_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), (2, self.rect.height / 2))
        
        
        collision_rects = [sprite.rect for sprite in self.collision_sprites]
        #collisions
        #collisions on floor
        self.on_surface["floor"] = True if floor_rect.collidelist(collision_rects) >= 0 else False
        
        self.on_surface["right"] = True if right_side_rect.collidelist(collision_rects) >= 0 else False
        self.on_surface["left"] = True if left_side_rect.collidelist(collision_rects) >= 0 else False
        
        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, "moving")]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
        
        
    def update_timer(self):
        for timer in self.timer.values():
            timer.update()
    
    #run all methods in this method
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timer()
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()
        # print(self.timer["wall slide block"].active)