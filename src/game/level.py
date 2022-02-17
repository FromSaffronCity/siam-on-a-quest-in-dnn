import pygame
from src.game.config import *
from src.game.tile import Tile
from src.game.player import Player

class Level:
	def __init__(self):

		# level setup
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = CameraGroup()
		self.active_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()


		self.player = None
		self.game_over = False
		self.setup_level()


		

	def setup_level(self):
		
		repeat = 20

		for i in range(repeat):
			for row_index,row in enumerate(LEVEL_MAP):
				for col_index,col in enumerate(row):
					x = ( i * len(row) + col_index) * TILE_SIZE
					y = row_index * TILE_SIZE
					if col == 'X':
						Tile((x,y),[self.visible_sprites,self.collision_sprites])
					if col == 'P' and self.player is None:
						self.player = Player((x,y),[self.visible_sprites,self.active_sprites],self.collision_sprites, self.visible_sprites, self.active_sprites)

	def run(self, action):
		# run the entire game (level)

		self.player.intended_action = action

		self.active_sprites.update()
		self.visible_sprites.custom_draw(self.player)

		self.player.intended_action = -1

		if self.player.is_dead == True:
			self.game_over = True


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2(100, -120)

		# camera
		cam_left = CAMERA_BORDERS['left']
		cam_top = CAMERA_BORDERS['top']
		cam_width = self.display_surface.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
		cam_height = self.display_surface.get_size()[1] - (cam_top + CAMERA_BORDERS['bottom'])

		self.camera_rect = pygame.Rect(cam_left,cam_top,cam_width,cam_height)

	def custom_draw(self,player):


		# get the player offset 
		self.offset.x = player.rect.centerx - 100


		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)