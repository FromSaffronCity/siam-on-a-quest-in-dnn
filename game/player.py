import pygame

from game.config import *
from game.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, visible_sprites, active_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.direction.x = 1
        self.speed = 6
        self.gravity = 0.8
        self.jump_speed = 16
        self.collision_sprites = collision_sprites
        self.visible_sprites = visible_sprites
        self.active_sprites = active_sprites

        self.score = 0
        self.on_floor = False
        self.is_dead = False

        self.shoot_cooldown = 0
        self.intended_action = -1

    def apply_intended_action(self):
        if GAME_MODE == 1:
            if self.intended_action == JUMP and self.on_floor:
                self.direction.y = -self.jump_speed
            if self.intended_action == SHOOT:
                self.shoot()
        else:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and self.on_floor:
                self.direction.y = -self.jump_speed

            if keys[pygame.K_TAB]:
                self.shoot()

    def shoot(self):
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = 10
        Bullet((self.rect.right + 10, self.rect.top + TILE_SIZE // 2 - 10), [self.active_sprites, self.visible_sprites],
               self.collision_sprites)

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

                self.is_dead |= True

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def check_death(self):
        self.is_dead |= self.rect.y > 1000

    def update(self):

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.apply_intended_action()

        prev_x = self.rect.x
        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()

        if self.rect.x > prev_x:
            self.score += 1

        self.apply_gravity()
        self.vertical_collisions()
        self.check_death()
