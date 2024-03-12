import pygame
from pygame.math import Vector2
from .projectile import Projectile


class Tower(pygame.sprite.Sprite):
    def __init__(self, position, screen, sound_manager, *groups):
        super().__init__(*groups)
        self.screen = screen
        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/tower.png").convert_alpha(), (40, 40)
        )
        self.rect = self.image.get_rect(center=position)
        self.shoot_delay = 650
        self.last_shot = pygame.time.get_ticks()
        self.sound_manager = sound_manager

        # Play the placement sound.
        self.sound_manager.play_sound("tower_place")

    def update(self, enemies):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and enemies:

            # Find the closest enemy based on actual distance.
            closest_enemy = min(
                enemies,
                key=lambda enemy: Vector2(enemy.rect.center).distance_to(
                    self.rect.center
                ),
            )

            # Shoot at the closest enemy.
            Projectile(self.screen, self.rect.center, closest_enemy.rect.center)

            # Reset the shoot timer.
            self.last_shot = now

    def draw_range_indicator(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), self.rect.center, self.range, 1)
