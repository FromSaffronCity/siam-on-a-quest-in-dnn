		if keys[pygame.K_SPACE] and self.on_floor:
			self.direction.y = -self.jump_speed

		if keys[pygame.K_TAB]:
			self.shoot()
