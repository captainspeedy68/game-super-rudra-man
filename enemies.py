from settings import * 
from random import choice
from timer import Timer

class Tooth(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, collision_sprites):
		super().__init__(groups)
		self.frames, self.frame_index = frames, 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_frect(topleft = pos)
		self.z = Z_LAYERS['main']

		self.direction = choice((-1,1))
		self.collision_rects = [sprite.rect for sprite in collision_sprites]
		self.speed = 200

		self.hit_timer = Timer(250)

	def reverse(self):
		if not self.hit_timer.active:
			self.direction *= -1
			self.hit_timer.activate()

	def update(self, dt):
		self.hit_timer.update()

		# animate
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]
		self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

		# move 
		self.rect.x += self.direction * self.speed * dt

		# reverse direction 
		floor_rect_right = pygame.FRect(self.rect.bottomright, (1,1))
		floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1,1))
		wall_rect = pygame.FRect(self.rect.topleft + vector(-1,0), (self.rect.width + 2, 1))

		if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
		   floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or \
		   wall_rect.collidelist(self.collision_rects) != -1:
			self.direction *= -1


class Pearl(pygame.sprite.Sprite):
	def __init__(self, pos, groups, surf, direction, speed):
		self.pearl = True
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(center = pos + vector(50 * direction,0))
		self.direction = direction
		self.speed = speed
		self.z = Z_LAYERS['main']
		self.timers = {'lifetime': Timer(5000), 'reverse': Timer(250)}
		self.timers['lifetime'].activate()

	def reverse(self):
		if not self.timers['reverse'].active:
			self.direction *= -1 
			self.timers['reverse'].activate()

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()

		self.rect.x += self.direction * self.speed * dt
		if not self.timers['lifetime'].active:
			self.kill()