import pygame
from random import randint
from .settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, MINIMUM_SHOOT_DELAY
from .utilities.sound_manager import SoundManager
from .sprites.tower import Tower
from .sprites.enemy import Enemy
from .sprites.projectile import Projectile
from .sprites.princess import Princess


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # Load the background image.
        self.tower_zone_y_start = WINDOW_HEIGHT / 2
        self.princess_zone_y_start = WINDOW_HEIGHT - 50
        self.shoot_delay_reduction_per_wave = 75
        self.minimum_shoot_delay = MINIMUM_SHOOT_DELAY
        self.initialize_game()
        self.sound_manager = SoundManager()

    def initialize_game(self):
        """Initialize the game state. This method is called when the game is first started and when the game is reset."""
        self.score = 0
        self.running = True
        self.game_over = False
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.princess_group = pygame.sprite.Group()
        self.princess = Princess(self.princess_group)
        Projectile.all_projectiles = pygame.sprite.Group()
        self.max_towers = 5
        self.current_wave = 0
        self.wave_enemies_remaining = 0
        self.spawn_enemy_timer = 1000
        self.between_wave_timer = 3000

    def run(self):
        while self.running:
            if not self.game_over:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
            else:
                self.display_game_over_screen()
        pygame.quit()

    def display_game_over_screen(self):
        self.window.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        self.window.blit(
            game_over_text,
            (
                WINDOW_WIDTH // 2 - game_over_text.get_rect().width // 2,
                WINDOW_HEIGHT // 3,
            ),
        )
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        self.window.blit(
            restart_text,
            (
                WINDOW_WIDTH // 2 - restart_text.get_rect().width // 2,
                WINDOW_HEIGHT // 2,
            ),
        )
        exit_text = font.render("Press ESC to Quit", True, (255, 255, 255))
        self.window.blit(
            exit_text,
            (
                WINDOW_WIDTH // 2 - exit_text.get_rect().width // 2,
                WINDOW_HEIGHT // 2 + 100,
            ),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.initialize_game()
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                mouse_pos = pygame.mouse.get_pos()
                if self.tower_zone_y_start < mouse_pos[1]:
                    if len(self.towers) < self.max_towers:

                        # Pass the window to the Tower's constructor for drawing range indicators.
                        Tower(mouse_pos, self.window, self.sound_manager, self.towers)

    def reduce_tower_shoot_delay(self):
        for tower in self.towers:
            new_shoot_delay = max(
                self.minimum_shoot_delay,
                tower.shoot_delay - self.shoot_delay_reduction_per_wave,
            )
            tower.shoot_delay = new_shoot_delay

    def update(self):
        if not self.game_over:
            self.towers.update(self.enemies)
            self.enemies.update()
            Projectile.all_projectiles.update()

            if pygame.time.get_ticks() % 150 == 0:
                self.enemies.add(Enemy(self.current_wave, self.enemies))

            hits = pygame.sprite.groupcollide(
                self.enemies, Projectile.all_projectiles, True, True
            )

            if hits:
                self.sound_manager.play_sound("arrow_hit")

            for hit in hits:
                self.score += 10

            # Check if an enemy has reached the princess.
            for enemy in self.enemies:
                if enemy.rect.top > self.princess_zone_y_start:
                    self.game_over = True

                    # Play the game over sound.
                    self.sound_manager.play_sound("game_over")
                    break

        if self.wave_enemies_remaining > 0 and self.spawn_enemy_timer <= 0:

            # Spawn an enemy and reset the timer.
            self.enemies.add(Enemy(self.current_wave, self.enemies))
            self.wave_enemies_remaining -= 1
            self.spawn_enemy_timer = 1000
        elif self.wave_enemies_remaining == 0:
            if self.between_wave_timer <= 0:

                # Start the next wave.
                self.current_wave += 1

                # Play the new wave sound.
                self.sound_manager.play_sound("new_wave")

                self.wave_enemies_remaining = self.current_wave * 5

                # Reset timer for next wave.
                self.between_wave_timer = 3000

                # Reduce the shoot delay for all towers.
                self.reduce_tower_shoot_delay()
            else:
                # Countdown to the next wave.
                self.between_wave_timer -= self.clock.get_time()

        if self.spawn_enemy_timer > 0:
            self.spawn_enemy_timer -= self.clock.get_time()

    def draw_text(self, text, font_size, color, x, y):
        font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        text = font.render(text, True, color)
        text_rect = text.get_rect(topleft=(x, y))
        self.window.blit(text, text_rect)

    def draw(self):

        # Fill background color.
        sand_color = (194, 178, 128)
        grass_color = (19, 109, 21)

        # calculate the height of each section.
        mid_point = WINDOW_HEIGHT // 2

        # Fill the top half sand color.
        pygame.draw.rect(self.window, sand_color, (0, 0, WINDOW_WIDTH, mid_point))

        # Fill the bottom half grass color.
        pygame.draw.rect(
            self.window, grass_color, (0, mid_point, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        # Draw the line for the princess zone.
        pygame.draw.line(
            self.window,
            (128, 128, 128),
            (0, self.princess_zone_y_start),
            (WINDOW_WIDTH, self.princess_zone_y_start),
            5,
        )

        # Draw all the sprites.
        self.towers.draw(self.window)
        self.enemies.draw(self.window)
        self.princess_group.draw(self.window)
        Projectile.all_projectiles.draw(self.window)

        # Draw UI elements.
        self.draw_text(f"Score: {self.score}", 24, (0, 0, 0), 10, 10)
        self.draw_text(f"Wave: {self.current_wave}", 24, (0, 0, 0), 10, 40)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
