import pygame, sys
from level import Level
import numpy as np

from PIL import Image as im
from config import *


pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT,  SCREEN_HEIGHT))
pygame.display.set_caption("Siam On A Quest")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)
episode_cnt = 0
level = None


def take_snapshot():
	surf = pygame.display.get_surface()
	x = pygame.surfarray.array3d(surf)
	x = np.fliplr(np.rot90(x, 3))
	data = im.fromarray(x)
	data.save('original.png')

	target_pixel = 30
	x = x.reshape((target_pixel, SCREEN_HEIGHT // target_pixel, target_pixel, SCREEN_HEIGHT // target_pixel, 3)).max(3).max(1)
	data = im.fromarray(x)
	data.save('sampled.png')


def show_text():
	episode_txt = font.render(f"Episode: {episode_cnt}" , True, (255, 255, 255))
	screen.blit(episode_txt, (10, 10))

	score_txt = font.render(f"Score: {level.player.score//5}" , True, (255, 255, 255))
	screen.blit(score_txt, (screen.get_width() - 120, 10))




def start():
	global episode_cnt, level

	level = Level()
	game_paused = 0
	episode_cnt += 1

	while True:
		
		if level.game_over:
			start()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					take_snapshot()
				elif event.key == pygame.K_q:
					pygame.quit()
					sys.exit()
				elif event.key == pygame.K_r:
					episode_cnt = 0
					start()
				elif event.key == pygame.K_p:
					game_paused ^= 1

		if game_paused:
			continue

		screen.fill(BG_COLOR)
		level.run()
		show_text()

		pygame.display.update()

		# take_snapshot()
		clock.tick(50)



if __name__ == '__main__':
	start()



