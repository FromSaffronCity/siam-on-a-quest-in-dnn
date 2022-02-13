import pygame
from config import *
from tile import Tile
from player import Player

class Level:
	def __init__(self):

		# level setup
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = CameraGroup()
		self.active_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()


		self.player = None
		self.setup_level()
		


	def setup_level(self):
		
		repeat = 50

		for i in range(repeat):
			for row_index,row in enumerate(LEVEL_MAP):
				for col_index,col in enumerate(row):
					x = ( i * len(row) + col_index) * TILE_SIZE
					y = row_index * TILE_SIZE
					if col == 'X':
						Tile((x,y),[self.visible_sprites,self.collision_sprites])
					if col == 'P' and self.player is None:
						self.player = Player((x,y),[self.visible_sprites,self.active_sprites],self.collision_sprites)

	def run(self):
		# run the entire game (level)
		self.active_sprites.update()
		self.visible_sprites.custom_draw(self.player)

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2(100, -20)

		# center camera setup 
		self.half_w = self.display_surface.get_size()[0] // 3

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