import pygame
import sys
import random
from background import Background
from button import Button
from audio import Audio
from upgrade import Upgrade
from game_storage import GameStorage
from reborn import RebornSystem
from skins import SkinManager

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
        self.background = Background(self.screen_width, self.screen_height)
        self.storage = GameStorage()
        self.reborn_system = RebornSystem() 
        self.skin_manager = SkinManager(self)

        self.clicks = 0
        self.total_clicks = 0
        self.click_power = 1 
        self.auto_click_rate = 0 
        self.auto_click_timer = 0 
        
        self.egg_is_pressed = False
        self.egg_press_timer = 0

        self.is_exiting = False
        self.exit_timer = 0
        self.show_reborn_window = False

        self.game_state = "menu"
        self.menu_offset = 0
        self.overlay_offset = -self.screen_width
        self.custom_overlay_offset = self.screen_width
        self.global_alpha = 0

        self._init_ui_elements()
        self.setup_upgrades()
        self.load_game_data()
        self.audio.load_background_music() 
        
        self.clock = pygame.time.Clock()
        self.running = True

    def _init_ui_elements(self):
        logo_img = pygame.image.load('textures/logo.png').convert_alpha()
        w_logo = int(self.screen_width * 0.6)
        h_logo = int(w_logo * (logo_img.get_height() / logo_img.get_width()))
        self.logo = pygame.transform.scale(logo_img, (w_logo, h_logo))
        self.logo_rect = self.logo.get_rect(center=(self.screen_width // 2, self.screen_height // 4))

        start_y = self.screen_height // 2 + self.logo.get_height() // 4 - 100
        hover_snd = self.audio.sounds.get('hover')
        
        self.btn_start = Button('textures/button_top.png', 'textures/shadow_button_top.png', (self.screen_width // 2, start_y), self.BUTTON_SIZE, hover_sound=hover_snd)
        self.btn_custom = Button('textures/custom_button.png', 'textures/shadow_custom_button.png', (self.screen_width // 2, start_y + 160), self.BUTTON_SIZE, hover_sound=hover_snd)
        self.btn_exit = Button('textures/button_exit.png', 'textures/shadow_button_exit.png', (self.screen_width // 2, start_y + 320), self.BUTTON_SIZE, hover_sound=hover_snd)

        sound_img = 'textures/sound.png' if self.audio.is_music_on else 'textures/no_sound.png'
        self.btn_sound = Button(sound_img, sound_img, (self.screen_width - 80, 80), (60, 60), center=False, hover_sound=hover_snd)
        self.btn_reborn = Button('textures/reborn.png', 'textures/reborn.png', (self.screen_width - 80, 160), (60, 60), center=False, hover_sound=hover_snd)

        win_original = pygame.image.load('textures/window.png').convert_alpha()
        self.reborn_window_surf = pygame.transform.scale(win_original, (int(self.screen_width * 0.9), int(self.screen_height * 0.9)))
        self.reborn_window_rect = self.reborn_window_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        
        x_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 80)
        self.close_txt_surf = x_font.render("X", True, (255, 105, 97))
        self.close_txt_rect = self.close_txt_surf.get_rect(topright=(self.reborn_window_rect.right - 50, self.reborn_window_rect.top + 30))

        self.reborn_title_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 120)
        self.reborn_main_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 64)
        self.reborn_sub_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 48)
        self.btn_confirm_reborn_rect = pygame.Rect(0, 0, 400, 100)

        self.game_overlay = pygame.transform.scale(pygame.image.load('textures/game_overlay.png').convert_alpha(), (self.screen_width, self.screen_height))

        title_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 48)
        self.counter_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 96)
        self.upgrades_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 144)
        self.stats_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 32)
        
        self.txt_title1 = title_font.render("Crack the egg", True, (143, 99, 79))
        self.txt_title2 = title_font.render("to get rich!", True, (143, 99, 79))

        self.egg_pos = (self.screen_width // 4, self.screen_height // 2 + 200)
        self.title_pos = (self.egg_pos[0], self.egg_pos[1] - 550)
        self.count_pos = (self.egg_pos[0], self.egg_pos[1] - 400)
        self.stats_pos = (self.count_pos[0], self.count_pos[1] + 100)
        self.upgrades_position = (self.screen_width * 3 // 4 + 27, self.screen_height // 2 - 386)

        self.icon_click = pygame.transform.scale(pygame.image.load('textures/click_icon.png').convert_alpha(), (40, 40))
        self.icon_sec = pygame.transform.scale(pygame.image.load('textures/sec_icon.png').convert_alpha(), (40, 40))

        self.shop_background = pygame.transform.scale(pygame.image.load('textures/shop2.png').convert_alpha(), (self.screen_width, self.screen_height))
        self.empty_btn_img = pygame.image.load('textures/button_empty.png').convert_alpha()

    def apply_skin(self, filename):
        original_egg = pygame.image.load(filename).convert_alpha()
        egg_w = int(self.screen_width * 0.25)
        egg_h = int(egg_w * (original_egg.get_height() / original_egg.get_width()))
        self.egg_image = pygame.transform.scale(original_egg, (egg_w, egg_h))
        
        pressed_w, pressed_h = int(egg_w * self.EGG_SHRINK_FACTOR), int(egg_h * self.EGG_SHRINK_FACTOR)
        self.egg_pressed_image = pygame.transform.scale(original_egg, (pressed_w, pressed_h))
        self.egg_pressed_image.fill((200, 200, 200, 255), special_flags=pygame.BLEND_RGBA_MULT)

    def _update_sound_button_icon(self, is_on):
        img_path = 'textures/sound.png' if is_on else 'textures/no_sound.png'
        norm = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (60, 60))
        self.btn_sound.normal_image = norm
        self.btn_sound.shadow_image = norm
        self.btn_sound.current_image = norm

    def load_game_data(self):
        data = self.storage.load()
        self.clicks = data.get('clicks', 0)
        self.total_clicks = data.get('total_clicks', 0)
        self.click_power = data.get('click_power', 1)
        self.auto_click_rate = data.get('auto_click_rate', 0)
        self.reborn_system.count = data.get('reborn_count', 0)
        
        self.skin_manager.unlocked_ids = data.get('unlocked_skins', ['default'])
        self.skin_manager.active_id = data.get('active_skin', 'default')
        
        active_skin = next((s for s in self.skin_manager.skins if s['id'] == self.skin_manager.active_id), self.skin_manager.skins[0])
        self.apply_skin(active_skin['filename'])
        
        is_music_on = data.get('music_on', True)
        self.audio.set_music_state(is_music_on)
        self._update_sound_button_icon(is_music_on)
        
        upgrades_data = data.get('upgrades', {})
        for u in self.upgrades:
            if u.name in upgrades_data:
                u.level = upgrades_data[u.name].get('level', 0)
                u.was_unlocked_once = upgrades_data[u.name].get('was_unlocked_once', False)
            u.check_unlock(self.total_clicks)

    def save_game_data(self):
        data = {
            'clicks': self.clicks,
            'total_clicks': self.total_clicks,
            'click_power': self.click_power,
            'auto_click_rate': self.auto_click_rate,
            'reborn_count': self.reborn_system.count, 
            'music_on': self.audio.is_music_on,
            'unlocked_skins': self.skin_manager.unlocked_ids, 
            'active_skin': self.skin_manager.active_id,       
            'upgrades': {u.name: {'level': u.level, 'was_unlocked_once': getattr(u, 'was_unlocked_once', False)} for u in self.upgrades}
        }
        self.storage.save(data)

    def setup_upgrades(self):
        icon_width, icon_height, spacing = 632, 144, 160 
        start_x = self.screen_width * 3 // 4 - icon_width // 2
        start_y = self.screen_height // 2 - 280
        
        self.upgrades = [
            Upgrade(d['name'], d['base_price'], d['price_growth'], d['icon'], d['effect_type'], d['effect_value'],
                    (start_x, start_y + i * spacing), (icon_width, icon_height), d['unlock_condition'])
            for i, d in enumerate(UPGRADES_CONFIG)
        ]
        self._check_upgrades_unlock()

    def _reset_progress(self):
        self.clicks = self.total_clicks = 0
        self.click_power = 1
        self.auto_click_rate = 0
        self.setup_upgrades() 

    def handle_events(self):
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.show_reborn_window: self.show_reborn_window = False
                elif self.game_state == "game": self.game_state = "transition_back"
                elif self.game_state == "custom": self.game_state = "transition_custom_back"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        mouse_pos = pygame.mouse.get_pos()

        if self.show_reborn_window:
            if mouse_clicked:
                if self.close_txt_rect.collidepoint(mouse_pos):
                    self.audio.play_sound('click')
                    self.show_reborn_window = False
                elif self.btn_confirm_reborn_rect.collidepoint(mouse_pos) and self.reborn_system.can_reborn(self.clicks):
                    self.audio.play_sound('buy')
                    self.reborn_system.do_reborn()
                    self._reset_progress()
                    self.show_reborn_window = False
            return 

        if self.game_state == "menu" and not self.is_exiting:
            button_clicked = True 
            if self.btn_exit.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.is_exiting = True
                self.exit_timer = 300 
            elif self.btn_custom.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.game_state = "transition_custom"
            elif self.btn_start.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.game_state = "transition" 
            elif self.btn_sound.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                is_on = not self.audio.is_music_on
                self.audio.set_music_state(is_on)
                self._update_sound_button_icon(is_on)
            elif self.btn_reborn.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.show_reborn_window = True
            else:
                button_clicked = False

            if mouse_clicked and self.logo_rect.collidepoint(mouse_pos) and not button_clicked:
                self.audio.play_sound('kukareku') 
        
        elif self.game_state == "game" and mouse_clicked:
            if self.egg_image.get_rect(center=self.egg_pos).collidepoint(mouse_pos):
                self.audio.play_sound('egg_click')
                actual_power = self.click_power * self.reborn_system.get_multiplier()
                self.clicks += actual_power
                self.total_clicks += actual_power
                self.egg_is_pressed = True
                self.egg_press_timer = self.EGG_PRESS_DURATION
                self._check_upgrades_unlock()
            else:
                self._handle_upgrade_purchases(mouse_pos)
                    
        elif self.game_state == "custom" and mouse_clicked:
            self.skin_manager.handle_click(mouse_pos)

    def _check_upgrades_unlock(self):
        for u in self.upgrades: u.check_unlock(self.total_clicks)

    def _handle_upgrade_purchases(self, mouse_pos):
        for u in self.upgrades:
            if u.rect.collidepoint(mouse_pos) and u.is_unlocked and self.clicks >= u.get_price():
                self.clicks -= u.get_price()
                u.purchase()
                self.audio.play_sound('buy') 
                
                if u.effect_type == 'click': self.click_power += u.effect_value
                elif u.effect_type == 'auto': self.auto_click_rate += u.effect_value
                self._check_upgrades_unlock()

    def update(self, dt):
        self.background.update()
        mouse_pos = pygame.mouse.get_pos()

        if self.is_exiting:
            self.exit_timer -= dt
            if self.exit_timer <= 0: self.running = False

        if self.egg_is_pressed:
            self.egg_press_timer -= dt
            if self.egg_press_timer <= 0: self.egg_is_pressed = False

        if self.game_state == "transition":
            self.menu_offset = min(self.screen_width, self.menu_offset + self.TRANSITION_SPEED * (dt/16))
            if self.menu_offset >= self.screen_width: self.game_state = "game"
        elif self.game_state == "transition_back":
            self.menu_offset = max(0, self.menu_offset - self.TRANSITION_SPEED * (dt/16))
            if self.menu_offset <= 0: self.game_state = "menu"
        elif self.game_state == "transition_custom":
            self.menu_offset = max(-self.screen_width, self.menu_offset - self.TRANSITION_SPEED * (dt/16))
            if self.menu_offset <= -self.screen_width: self.game_state = "custom"
        elif self.game_state == "transition_custom_back":
            self.menu_offset = min(0, self.menu_offset + self.TRANSITION_SPEED * (dt/16))
            if self.menu_offset >= 0: self.game_state = "menu"

        self.overlay_offset = -self.screen_width + self.menu_offset
        self.custom_overlay_offset = self.screen_width + self.menu_offset
        self.global_alpha = int(255 * (abs(self.menu_offset) / self.screen_width))

        if "transition" in self.game_state or self.game_state == "menu":
            if not self.show_reborn_window:
                for btn in [self.btn_start, self.btn_custom, self.btn_exit, self.btn_sound, self.btn_reborn]:
                    btn.update(mouse_pos)
            
        if self.game_state in ["transition", "transition_back", "game"]:
            for u in self.upgrades: u.hovered = u.rect.collidepoint(mouse_pos)
                
            if self.game_state == "game":
                self.auto_click_timer += dt
                if self.auto_click_timer >= 1000:
                    self.auto_click_timer -= 1000
                    if self.auto_click_rate > 0:
                        actual_rate = self.auto_click_rate * self.reborn_system.get_multiplier()
                        self.clicks += actual_rate
                        self.total_clicks += actual_rate
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
            mult = self.reborn_system.get_multiplier()
            click_surf = self.stats_font.render(f"{int(self.click_power * mult)}/click", True, (108, 73, 58))
            sec_surf = self.stats_font.render(f"{int(self.auto_click_rate * mult)}/sec", True, (108, 73, 58))
            
            for s in [click_surf, sec_surf, self.icon_click, self.icon_sec]: s.set_alpha(alpha)
            
            sx = self.stats_pos[0] - (self.icon_click.get_width() + click_surf.get_width() + 40 + self.icon_sec.get_width() + sec_surf.get_width()) // 2 + offset_x
            self.screen.blit(self.icon_click, (sx, self.stats_pos[1]))
            self.screen.blit(click_surf, (sx + 50, self.stats_pos[1] + 5))
            
            sx2 = sx + click_surf.get_width() + 90
            self.screen.blit(self.icon_sec, (sx2, self.stats_pos[1]))
            self.screen.blit(sec_surf, (sx2 + 50, self.stats_pos[1] + 5))

            upgrades_title = self.upgrades_font.render("UPGRADES", True, (108, 73, 58))
            upgrades_title.set_alpha(alpha)
            t_rect = upgrades_title.get_rect(center=self.upgrades_position)
            t_rect.x += offset_x
            self.screen.blit(upgrades_title, t_rect)

            for u in self.upgrades:
                u.draw(self.screen, offset_x, self.clicks >= u.get_price(), alpha)

        shake = random.randint(-4, 4) if self.egg_is_pressed else 0
        img = self.egg_pressed_image if self.egg_is_pressed else self.egg_image
        img.set_alpha(alpha)
        self.screen.blit(img, img.get_rect(center=(self.egg_pos[0] + offset_x + shake, self.egg_pos[1] + shake)))

    def draw_custom_scene(self, offset_x, alpha):
        self.shop_background.set_alpha(alpha)
        self.screen.blit(self.shop_background, (offset_x, 0))
        self.skin_manager.draw(self.screen, offset_x, alpha)

    def draw(self):
        self.background.draw(self.screen)
        
        if self.game_state == "menu":
            self.screen.blit(self.logo, self.logo_rect)
            for btn in [self.btn_start, self.btn_custom, self.btn_exit, self.btn_sound, self.btn_reborn]: 
                btn.draw(self.screen)
            
            if self.show_reborn_window:
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (0, 0))
                self.screen.blit(self.reborn_window_surf, self.reborn_window_rect)
                self.screen.blit(self.close_txt_surf, self.close_txt_rect)

                cy = self.screen_height // 2
                win_top, win_bottom = cy - int(self.screen_height * 0.40), cy + int(self.screen_height * 0.40)

                texts = [
                    (self.reborn_title_font.render("REBORN", True, (108, 73, 58)), win_top),
                    (self.reborn_main_font.render(f"number of reborns: {self.reborn_system.count}", True, (108, 73, 58)), win_top + 130),
                    (self.reborn_sub_font.render("Rebirths completely reset progress", True, (143, 99, 79)), cy - 80),
                    (self.reborn_sub_font.render(f"Cost: {self.reborn_system.get_cost()} clicks", True, (143, 99, 79)), cy),
                    (self.reborn_sub_font.render(f"Reward: x{self.reborn_system.get_multiplier() + 1} multiplier", True, (143, 99, 79)), cy + 80)
                ]
                
                for txt, y_pos in texts:
                    self.screen.blit(txt, (self.screen_width//2 - txt.get_width()//2, y_pos))

                can_reborn = self.reborn_system.can_reborn(self.clicks)
                btn_color = (96, 192, 96) if can_reborn else (255, 105, 97)
                t_btn = self.reborn_title_font.render("Reborn now" if can_reborn else "Not enough clicks!", True, btn_color)
                
                btn_w, btn_h = max(t_btn.get_width() + 100, 400), t_btn.get_height() + 40
                self.btn_confirm_reborn_rect.size = (btn_w, btn_h)
                self.btn_confirm_reborn_rect.center = (self.screen_width // 2, win_bottom - 80)
                
                self.screen.blit(pygame.transform.scale(self.empty_btn_img, (btn_w, btn_h)), self.btn_confirm_reborn_rect.topleft)
                self.screen.blit(t_btn, t_btn.get_rect(center=self.btn_confirm_reborn_rect.center))
            
        elif "transition" in self.game_state:
            if self.menu_offset > 0 or self.game_state == "transition": self.draw_game_scene(self.overlay_offset, self.global_alpha)
            elif self.menu_offset < 0 or self.game_state == "transition_custom": self.draw_custom_scene(self.custom_overlay_offset, self.global_alpha)
            
            l_rect = self.logo_rect.copy()
            l_rect.x += self.menu_offset
            self.screen.blit(self.logo, l_rect)

            for btn in [self.btn_start, self.btn_custom, self.btn_exit, self.btn_sound, self.btn_reborn]: 
                old_x = btn.rect.x
                btn.rect.x += self.menu_offset
                btn.draw(self.screen)
                btn.rect.x = old_x
            
        elif self.game_state == "game": self.draw_game_scene(0, 255)
        elif self.game_state == "custom": self.draw_custom_scene(0, 255)

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