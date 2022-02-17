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



def printImage(display_matrix):
	image = im.fromarray(display_matrix)
	image.save('original.png')


def take_snapshot():
	surf = pygame.display.get_surface()
	display_matrix = pygame.surfarray.array3d(surf)
	display_matrix = np.fliplr(np.rot90(display_matrix, 3))
	
	display_matrix = display_matrix.reshape((SHRINK_HEIGHT, SCREEN_HEIGHT // SHRINK_HEIGHT, SHRINK_HEIGHT, SCREEN_HEIGHT // SHRINK_HEIGHT, 3)).max(3).max(1)
	return display_matrix



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

					# for (id, frame) in enumerate(all_frames):
					# 	image = im.fromarray(frame)
					# 	image.save(f"img/original{id}.png")

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

		take_snapshot()
		clock.tick()



if __name__ == '__main__':
	start()



