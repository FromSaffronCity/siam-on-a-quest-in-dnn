import pygame
import sys
import numpy as np
from PIL import Image

if __name__ == '__main__':
    from level import Level
    from config import *
elif __name__ == 'game.game':
    from .level import Level
    from .config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_HEIGHT))
        pygame.display.set_caption("Siam On A Quest")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        # self.episode_cnt = 0
        self.level = None

        self.game_paused = 0

    def print_image(self, display_matrix):
        image = Image.fromarray(display_matrix)
        image.save('original.png')

    def show_text(self, episode):
        episode_txt = self.font.render(f"Episode: {episode}", True, (255, 255, 255))
        self.screen.blit(episode_txt, (10, 10))

        score_txt = self.font.render(f"Score: {self.level.player.score // 5}", True, (255, 255, 255))
        self.screen.blit(score_txt, (self.screen.get_width() - 120, 10))

    def take_snapshot(self):
        surf = pygame.display.get_surface()
        display_matrix = pygame.surfarray.array3d(surf)
        display_matrix = np.fliplr(np.rot90(display_matrix, 3))

        display_matrix = display_matrix.reshape((SHRINK_HEIGHT, SCREEN_HEIGHT // SHRINK_HEIGHT, SHRINK_HEIGHT, SCREEN_HEIGHT // SHRINK_HEIGHT, 3)).max(3).max(1)
        return display_matrix

    def reset(self, episode):
        self.level = Level()
        self.game_paused = 0
        self.step(0, episode)
        return self.take_snapshot()

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    image = self.take_snapshot()
                    self.print_image(image)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    # self.episode_cnt = 0
                    self.reset(1)
                elif event.key == pygame.K_p:
                    self.game_paused ^= 1

    def step(self, action, episode):
        self.handle_user_input()

        if self.game_paused:
            return

        self.screen.fill(BG_COLOR)
        self.level.run(action)
        self.show_text(episode)

        pygame.display.update()

        return_state = self.take_snapshot()
        return_reward = DEATH_PENALTY if self.level.game_over else SURVIVAL_REWARD
        return_done = self.level.game_over
        return_score = self.level.player.score // 5

        self.clock.tick()
        # if self.level.game_over:
        # 	self.reset()

        return return_state, return_reward, return_done, return_score

if __name__ == '__main__':
    game = Game()
    count = 1

    while True:
        init_state = game.reset(count)
        game.print_image(init_state)
        while True:
            action = 1
            (next_state, reward, done, score) = game.step(action, count)
            count = count + 1
            if done:
                break
