import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "tower_place": pygame.mixer.Sound("assets/sounds/tower_place.wav"),
            "arrow_hit": pygame.mixer.Sound("assets/sounds/hit.wav"),
            "new_wave": pygame.mixer.Sound("assets/sounds/new_wave.wav"),
            "game_over": pygame.mixer.Sound("assets/sounds/game_over.wav"),
        }

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
