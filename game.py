import pygame
import sys
import random
from background import Background
from button import Button
from audio import Audio
from upgrade import Upgrade
from game_storage import GameStorage

UPGRADES_CONFIG = [
    {'name': 'strong_fingers', 'base_price': 10, 'price_growth': 1.5, 'icon': 'textures/upgrades/strong_fingers.png', 'effect_type': 'click', 'effect_value': 1, 'unlock_condition': 0},
    {'name': 'auto_clicker', 'base_price': 50, 'price_growth': 1.7, 'icon': 'textures/upgrades/auto_clicker.png', 'effect_type': 'auto', 'effect_value': 1, 'unlock_condition': 1000},
    {'name': 'golden_touch', 'base_price': 200, 'price_growth': 1.8, 'icon': 'textures/upgrades/golden_touch.png', 'effect_type': 'click', 'effect_value': 5, 'unlock_condition': 5000},
    {'name': 'egg_farm', 'base_price': 1000, 'price_growth': 1.9, 'icon': 'textures/upgrades/egg_farm.png', 'effect_type': 'auto', 'effect_value': 10, 'unlock_condition': 20000},
    {'name': 'mega_drill', 'base_price': 5000, 'price_growth': 2.0, 'icon': 'textures/upgrades/mega_drill.png', 'effect_type': 'click', 'effect_value': 50, 'unlock_condition': 50000}
]

class Game:
    def __init__(self):
        self.FPS = 60
        self.TRANSITION_SPEED = 20
        self.BUTTON_SIZE = (632, 144)
        self.EGG_PRESS_DURATION = 100
        self.EGG_SHRINK_FACTOR = 0.95

        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Crack the Record!")
        self.screen_width, self.screen_height = self.screen.get_size()

        self.audio = Audio()
        self.audio.load_sounds()
        self.audio.load_background_music()
        self.background = Background(self.screen_width, self.screen_height)
        self.storage = GameStorage()

        self.clicks = 0
        self.total_clicks = 0
        self.click_power = 1 
        self.auto_click_rate = 0 
        self.auto_click_timer = 0 
        
        self.egg_is_pressed = False
        self.egg_press_timer = 0

        self.game_state = "menu"
        self.menu_offset = 0
        self.overlay_offset = -self.screen_width
        self.global_alpha = 0

        self._init_ui_elements()
        self.setup_upgrades()
        self.load_game_data()
        
        self.clock = pygame.time.Clock()
        self.running = True

    def _init_ui_elements(self):
        logo_img = pygame.image.load('textures/logo.png').convert_alpha()
        w_logo = int(self.screen_width * 0.6)
        h_logo = int(w_logo * (logo_img.get_height() / logo_img.get_width()))
        self.logo = pygame.transform.scale(logo_img, (w_logo, h_logo))
        self.logo_rect = self.logo.get_rect(center=(self.screen_width // 2, self.screen_height // 4))

        start_y = self.screen_height // 2 + self.logo.get_height() // 4
        hover_snd = self.audio.sounds.get('hover')
        self.btn_start = Button('textures/button_top.png', 'textures/shadow_button_top.png', 
                                (self.screen_width // 2, start_y), self.BUTTON_SIZE, hover_sound=hover_snd)
        self.btn_exit = Button('textures/button_exit.png', 'textures/shadow_button_exit.png', 
                               (self.screen_width // 2, start_y + 200), self.BUTTON_SIZE, hover_sound=hover_snd)

        original_egg = pygame.image.load('textures/egg.png').convert_alpha()
        egg_w = int(self.screen_width * 0.25)
        egg_h = int(egg_w * (original_egg.get_height() / original_egg.get_width()))
        self.egg_image = pygame.transform.scale(original_egg, (egg_w, egg_h))
        
        original_shadow = pygame.image.load('textures/egg_shadow.png').convert_alpha()
        pressed_w, pressed_h = int(egg_w * self.EGG_SHRINK_FACTOR), int(egg_h * self.EGG_SHRINK_FACTOR)
        self.egg_pressed_image = pygame.transform.scale(original_shadow, (pressed_w, pressed_h))

        overlay_img = pygame.image.load('textures/game_overlay.png').convert_alpha()
        self.game_overlay = pygame.transform.scale(overlay_img, (self.screen_width, self.screen_height))

        title_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 48)
        self.counter_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 96)
        self.upgrades_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 144)
        
        self.txt_title1 = title_font.render("Crack the egg", True, (143, 99, 79))
        self.txt_title2 = title_font.render("to get rich!", True, (143, 99, 79))

        self.egg_pos = (self.screen_width // 4, self.screen_height // 2 + 200)
        self.title_pos = (self.egg_pos[0], self.egg_pos[1] - 550)
        self.count_pos = (self.egg_pos[0], self.egg_pos[1] - 400)
        self.upgrades_position = (self.screen_width * 3 // 4 + 27, self.screen_height // 2 - 386)

    def load_game_data(self):
        data = self.storage.load()
        if not data:
            return 
            
        self.clicks = data.get('clicks', 0)
        self.total_clicks = data.get('total_clicks', 0)
        self.click_power = data.get('click_power', 1)
        self.auto_click_rate = data.get('auto_click_rate', 0)
        
        upgrades_data = data.get('upgrades', {})
        for u in self.upgrades:
            if u.name in upgrades_data:
                u_data = upgrades_data[u.name]
                u.level = u_data.get('level', 0)
                u.was_unlocked_once = u_data.get('was_unlocked_once', False)
                u.check_unlock(self.total_clicks)

    def save_game_data(self):
        data = {
            'clicks': self.clicks,
            'total_clicks': self.total_clicks,
            'click_power': self.click_power,
            'auto_click_rate': self.auto_click_rate,
            'upgrades': {u.name: {'level': getattr(u, 'level', 0), 'was_unlocked_once': getattr(u, 'was_unlocked_once', False)} for u in self.upgrades}
        }
        self.storage.save(data)

    def setup_upgrades(self):
        icon_width, icon_height = 632, 144 
        start_x = self.screen_width * 3 // 4 - icon_width // 2
        start_y = self.screen_height // 2 - 280
        spacing = 160 
        
        self.upgrades = []
        for i, d in enumerate(UPGRADES_CONFIG):
            u = Upgrade(d['name'], d['base_price'], d['price_growth'], d['icon'], d['effect_type'], d['effect_value'],
                        (start_x, start_y + i * spacing), (icon_width, icon_height), d['unlock_condition'])
            u.check_unlock(self.total_clicks)
            self.upgrades.append(u)

    def handle_events(self):
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "menu": 
                        self.running = False
                    elif self.game_state == "game": 
                        self.game_state = "transition_back"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        mouse_pos = pygame.mouse.get_pos()

        if self.game_state == "menu":
            if mouse_clicked and self.logo_rect.collidepoint(mouse_pos):
                self.audio.play_sound('kukareku') 
            if self.btn_exit.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.running = False
            if self.btn_start.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.game_state = "transition" 
        
        elif self.game_state == "game":
            egg_rect = self.egg_image.get_rect(center=self.egg_pos)
            if mouse_clicked:
                if egg_rect.collidepoint(mouse_pos):
                    self.audio.play_sound('egg_click')
                    self.clicks += self.click_power
                    self.total_clicks += self.click_power
                    self.egg_is_pressed = True
                    self.egg_press_timer = self.EGG_PRESS_DURATION
                    self._check_upgrades_unlock()
                else:
                    self._handle_upgrade_purchases(mouse_pos)

    def _check_upgrades_unlock(self):
        for u in self.upgrades: 
            u.check_unlock(self.total_clicks)

    def _handle_upgrade_purchases(self, mouse_pos):
        for u in self.upgrades:
            if u.rect.collidepoint(mouse_pos) and u.is_unlocked:
                price = u.get_price()
                if self.clicks >= price:
                    self.clicks -= price
                    u.purchase()
                    self.audio.play_sound('buy') 
                    
                    if u.effect_type == 'click':
                        self.click_power += u.effect_value
                    elif u.effect_type == 'auto':
                        self.auto_click_rate += u.effect_value
                        
                    self._check_upgrades_unlock()

    def update(self, dt):
        self.background.update()
        mouse_pos = pygame.mouse.get_pos()

        if self.egg_is_pressed:
            self.egg_press_timer -= dt
            if self.egg_press_timer <= 0: 
                self.egg_is_pressed = False

        if self.game_state == "transition":
            self.menu_offset = min(self.screen_width, self.menu_offset + self.TRANSITION_SPEED * (dt/16))
            if self.menu_offset >= self.screen_width: 
                self.game_state = "game"
        elif self.game_state == "transition_back":
            self.menu_offset = max(0, self.menu_offset - self.TRANSITION_SPEED * (dt/16))
            if self.menu_offset <= 0: 
                self.game_state = "menu"

        self.overlay_offset = -self.screen_width + self.menu_offset
        self.global_alpha = int(255 * (self.menu_offset / self.screen_width))

        if self.game_state in ["menu", "transition", "transition_back"]:
            self.btn_start.update(mouse_pos)
            self.btn_exit.update(mouse_pos)
            
        if self.game_state in ["transition", "transition_back", "game"]:
            for u in self.upgrades:
                u.hovered = u.rect.collidepoint(mouse_pos)
                
            if self.game_state == "game":
                self.auto_click_timer += dt
                if self.auto_click_timer >= 1000:
                    self.auto_click_timer -= 1000
                    if self.auto_click_rate > 0:
                        self.clicks += self.auto_click_rate
                        self.total_clicks += self.auto_click_rate
                        self._check_upgrades_unlock()

    def draw_game_scene(self, offset_x, alpha):
        self.game_overlay.set_alpha(alpha)
        self.screen.blit(self.game_overlay, (offset_x, 0))

        c_surf = self.counter_font.render(str(int(self.clicks)), True, (108, 73, 58))
        
        self.txt_title1.set_alpha(alpha)
        self.txt_title2.set_alpha(alpha)
        c_surf.set_alpha(alpha)

        self.screen.blit(self.txt_title1, (self.title_pos[0] + offset_x - self.txt_title1.get_width()//2, self.title_pos[1] - 25))
        self.screen.blit(self.txt_title2, (self.title_pos[0] + offset_x - self.txt_title2.get_width()//2, self.title_pos[1] + 25))
        self.screen.blit(c_surf, (self.count_pos[0] + offset_x - c_surf.get_width()//2, self.count_pos[1] - c_surf.get_height()//2))

        if alpha > 0:
            upgrades_title = self.upgrades_font.render("UPGRADES", True, (108, 73, 58))
            upgrades_title.set_alpha(alpha)
            t_rect = upgrades_title.get_rect(center=self.upgrades_position)
            t_rect.x += offset_x
            self.screen.blit(upgrades_title, t_rect)

            for u in self.upgrades:
                can_afford = self.clicks >= u.get_price()
                u.draw(self.screen, offset_x, can_afford, alpha)

        shake = random.randint(-4, 4) if self.egg_is_pressed else 0
        img = self.egg_pressed_image if self.egg_is_pressed else self.egg_image
        
        img.set_alpha(alpha)
        rect = img.get_rect(center=(self.egg_pos[0] + offset_x + shake, self.egg_pos[1] + shake))
        self.screen.blit(img, rect)

    def draw(self):
        self.background.draw(self.screen)
        
        if self.game_state == "menu":
            self.screen.blit(self.logo, self.logo_rect)
            self.btn_start.draw(self.screen)
            self.btn_exit.draw(self.screen)
            
        elif self.game_state in ["transition", "transition_back"]:
            self.draw_game_scene(self.overlay_offset, self.global_alpha)
            
            l_rect = self.logo_rect.copy()
            l_rect.x += self.menu_offset
            self.screen.blit(self.logo, l_rect)

            for btn in [self.btn_start, self.btn_exit]:
                old_x = btn.rect.x
                btn.rect.x += self.menu_offset
                btn.draw(self.screen)
                btn.rect.x = old_x
            
        elif self.game_state == "game":
            self.draw_game_scene(0, 255)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS) 
            self.handle_events()
            self.update(dt)
            self.draw()
            
        self.save_game_data()
        pygame.quit()
        sys.exit()