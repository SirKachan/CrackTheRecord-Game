import pygame
import sys
from background import Background

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Crack the Record!")
        self.screen_width, self.screen_height = self.screen.get_size()

        self.background = Background(self.screen_width, self.screen_height)

        logo_img = pygame.image.load('textures/logo.png').convert_alpha()
        w_logo = int(self.screen_width * 0.6)
        h_logo = int(w_logo * (logo_img.get_height() / logo_img.get_width()))
        self.logo = pygame.transform.scale(logo_img, (w_logo, h_logo))
        self.logo_rect = self.logo.get_rect(center=(self.screen_width // 2, self.screen_height // 4))

        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.background.update()

    def draw(self):

        self.background.draw(self.screen)

        if self.logo:
            self.screen.blit(self.logo, self.logo_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()