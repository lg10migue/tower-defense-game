import pygame
from ..settings import WINDOW_WIDTH, WINDOW_HEIGHT


class Princess(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/princess.png").convert_alpha(), (40, 40)
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT
