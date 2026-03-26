import pygame
import sys
from background import Background
from button import Button

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Crack the Record!")
        self.screen_width, self.screen_height = self.screen.get_size()
        self.BUTTON_SIZE = (632, 144)
        self.background = Background(self.screen_width, self.screen_height)
        logo_img = pygame.image.load('textures/logo.png').convert_alpha()
        w_logo = int(self.screen_width * 0.6)
        h_logo = int(w_logo * (logo_img.get_height() / logo_img.get_width()))
        self.logo = pygame.transform.scale(logo_img, (w_logo, h_logo))
        self.logo_rect = self.logo.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        logo_height = self.logo.get_height()
        start_y = self.screen_height // 2 + logo_height // 4
        btn_spacing = 200
        self.btn_start = Button('textures/button_top.png', 'textures/shadow_button_top.png', (self.screen_width // 2, start_y), self.BUTTON_SIZE            )
        self.btn_exit = Button('textures/button_exit.png', 'textures/shadow_button_exit.png', (self.screen_width // 2, start_y + btn_spacing), self.BUTTON_SIZE)     
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        mouse_pos = pygame.mouse.get_pos()
        if self.btn_exit.is_clicked(mouse_pos, mouse_clicked):
            self.running = False # Выход из игры
        if self.btn_start.is_clicked(mouse_pos, mouse_clicked):
            print("Клик по СТАРТ! В будущем тут будет переход к яйцу.")

    def update(self):
        self.background.update()
        mouse_pos = pygame.mouse.get_pos()
        self.btn_start.update(mouse_pos)
        self.btn_exit.update(mouse_pos)

    def draw(self):       
        self.background.draw(self.screen)
        if self.logo:
            self.screen.blit(self.logo, self.logo_rect)
        self.btn_start.draw(self.screen)
        self.btn_exit.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()