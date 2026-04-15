import pygame

class Audio:
    def __init__(self):
        self.sounds = {}
        self.is_music_on = True
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    def load_sounds(self):
        files = {
            'hover': 'sounds/button_hover.wav',
            'click': 'sounds/button_click.wav',
            'kukareku': 'sounds/kukareku.wav',
            'egg_click': 'sounds/egg_click.wav',
            'buy': 'sounds/buy.wav',
            'reborn': 'sounds/reborn.wav',
            'pre_reborn': 'sounds/pre_reborn.wav'
        }

        for name, path in files.items():
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(0.4)

    def load_background_music(self):
        pygame.mixer.music.load('sounds/music.wav')
        pygame.mixer.music.set_volume(1.0 if self.is_music_on else 0)
        pygame.mixer.music.play(-1, 0.0)

    def set_music_state(self, is_on):
        self.is_music_on = is_on
        pygame.mixer.music.set_volume(1.0 if self.is_music_on else 0)

    def play_sound(self, name):
        self.sounds[name].play()
        
    def play_pre_reborn_music(self):
        if self.is_music_on: # Проверяем, чтобы музыка не играла, если она выключена в настройках
            self.sounds['pre_reborn'].play(loops=-1) # параметр loops=-1 зацикливает звук бесконечно

    def stop_pre_reborn_music(self):
        self.sounds['pre_reborn'].stop() # Останавливаем воспроизведение