import pygame

from game.config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect(topleft=pos)

        self.collision_sprites = collision_sprites
        self.speed = 12
        self.init_x = pos[0]

    def grid_collisions(self):

        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.kill()
                return

    def update(self):
        self.rect.x += self.speed

        if self.rect.x > self.init_x + SCREEN_HEIGHT * 2:
            self.kill()
            return

        self.grid_collisions()
