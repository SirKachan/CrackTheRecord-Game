import pygame

class Audio:
    def __init__(self):
        self.is_music_on = True
        self.sounds = {}
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    def load_sounds(self):
        files = {
            'hover': 'sounds/button_hover.wav',
            'click': 'sounds/button_click.wav',
            'kukareku': 'sounds/kukareku.wav',
        }

        for name, path in files.items():
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(0.4)
        return self.sounds

    def load_background_music(self):
        path = 'sounds/music.wav'
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(1.0 if self.is_music_on else 0)
        pygame.mixer.music.play(-1, 0.0)

    def set_music_state(self, is_on):
        self.is_music_on = is_on
        pygame.mixer.music.set_volume(1.0 if self.is_music_on else 0)

    def play_sound(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()