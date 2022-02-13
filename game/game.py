import pygame, sys
from level import Level
import numpy as np

from PIL import Image as im
from config import *




pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT,  SCREEN_HEIGHT))
pygame.display.set_caption("Siam On A Quest")
clock = pygame.time.Clock()


def take_snapshot():
	surf = pygame.display.get_surface()
	x = pygame.surfarray.array3d(surf)
	x = np.fliplr(np.rot90(x, 3))
	data = im.fromarray(x)
	data.save('original.png')
	x = x.reshape((30, 720 // 30, 30, 720 // 30, 3)).max(3).max(1)
	# x = x.reshape((80, 720 // 80, 80, 720 // 80, 3)).max(3).max(1)
	data = im.fromarray(x)
	data.save('sampled.png')



def start():
	level = Level()
	game_paused = 0

	while True:
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
					start()
				elif event.key == pygame.K_p:
					game_paused ^= 1

		if game_paused:
			continue
		
		screen.fill(BG_COLOR)
		level.run()

		pygame.display.update()
		clock.tick(60)



if __name__ == '__main__':
	start()



