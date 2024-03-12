import pygame
from random import randint
from ..settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, wave_number, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/goblin.png").convert_alpha(), (20, 20)
        )
        self.rect = self.image.get_rect(center=(randint(0, WINDOW_WIDTH), 0))
        self.speed = 1.5 + (wave_number * 0.05)
        self.health = 100 + wave_number * 5

    def update(self):

        # Move downwards.
        self.rect.y += self.speed

        # Kill the sprite if it moves past the bottom of the screen.
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
