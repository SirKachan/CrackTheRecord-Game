import pygame

class Background:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.image = pygame.image.load('textures/sky.png').convert()
        scale = screen_height / self.image.get_height()
        new_width = int(self.image.get_width() * scale)
        self.image = pygame.transform.scale(self.image, (new_width, screen_height))

        self.width = self.image.get_width()
        self.x = 0
        self.scroll_speed = 0.5
    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -self.width:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 0))
        if self.x < self.screen_width - self.width:
            screen.blit(self.image, (self.x + self.width, 0))