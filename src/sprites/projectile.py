import pygame
from pygame import Vector2


class Projectile(pygame.sprite.Sprite):
    all_projectiles = pygame.sprite.Group()

    def __init__(self, screen, position, target_pos):
        super().__init__(self.all_projectiles)
        self.screen = screen
        self.original_image = pygame.transform.scale(
            pygame.image.load("assets/images/arrow.png").convert_alpha(), (10, 10)
        )
        self.position = Vector2(position)
        self.target_pos = Vector2(target_pos)
        self.velocity = self.target_pos - self.position
        self.velocity.scale_to_length(5)

        # Calculate the angle of the projectile.
        self.angle = self.velocity.angle_to(Vector2(0, -1))

        # Rotate the projectile.
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Set the position of the projectile.
        self.rect = self.image.get_rect(center=position)

    def update(self):
        # Update the position of the vector.
        self.position += self.velocity

        # Update the rect.
        self.rect.center = self.position

        # Remove the projectile if it moves off the screen.
        if not self.screen.get_rect().contains(self.rect):
            self.kill()
