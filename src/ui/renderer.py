import pygame
import random
from src.ui.button import Button
from src.core.config import BUTTON_SIZE, EGG_SHRINK_FACTOR

class Renderer:
    def __init__(self, screen, audio):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.audio = audio
        
        self.egg_image = None
        self.egg_pressed_image = None
        self._init_ui_elements()

    def _init_ui_elements(self):
        logo_img = pygame.image.load('textures/logo.png').convert_alpha()
        w_logo = int(self.screen_width * 0.6)
        h_logo = int(w_logo * (logo_img.get_height() / logo_img.get_width()))
        self.logo = pygame.transform.scale(logo_img, (w_logo, h_logo))
        self.logo_rect = self.logo.get_rect(center=(self.screen_width // 2, self.screen_height // 4))

        start_y = self.screen_height // 2 + self.logo.get_height() // 4 - 100
        hover_snd = self.audio.sounds.get('hover')
        
        self.btn_start = Button('textures/button_top.png', 'textures/shadow_button_top.png', (self.screen_width // 2, start_y), BUTTON_SIZE, hover_sound=hover_snd)
        self.btn_custom = Button('textures/custom_button.png', 'textures/shadow_custom_button.png', (self.screen_width // 2, start_y + 160), BUTTON_SIZE, hover_sound=hover_snd)
        self.btn_exit = Button('textures/button_exit.png', 'textures/shadow_button_exit.png', (self.screen_width // 2, start_y + 320), BUTTON_SIZE, hover_sound=hover_snd)

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

    def update_sound_button_icon(self, is_on):
        img_path = 'textures/sound.png' if is_on else 'textures/no_sound.png'
        norm = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (60, 60))
        self.btn_sound.normal_image = norm
        self.btn_sound.shadow_image = norm
        self.btn_sound.current_image = norm

    def apply_skin(self, filename):
        original_egg = pygame.image.load(filename).convert_alpha()
        egg_w = int(self.screen_width * 0.25)
        egg_h = int(egg_w * (original_egg.get_height() / original_egg.get_width()))
        self.egg_image = pygame.transform.scale(original_egg, (egg_w, egg_h))
        
        pressed_w, pressed_h = int(egg_w * EGG_SHRINK_FACTOR), int(egg_h * EGG_SHRINK_FACTOR)
        self.egg_pressed_image = pygame.transform.scale(original_egg, (pressed_w, pressed_h))
        self.egg_pressed_image.fill((200, 200, 200, 255), special_flags=pygame.BLEND_RGBA_MULT)

    def draw_game_scene(self, offset_x, alpha, stats, reborn_system, upgrades_manager):
        self.game_overlay.set_alpha(alpha)
        self.screen.blit(self.game_overlay, (offset_x, 0))

        c_surf = self.counter_font.render(str(int(stats.clicks)), True, (108, 73, 58))
        self.txt_title1.set_alpha(alpha)
        self.txt_title2.set_alpha(alpha)
        c_surf.set_alpha(alpha)

        self.screen.blit(self.txt_title1, (self.title_pos[0] + offset_x - self.txt_title1.get_width()//2, self.title_pos[1] - 25))
        self.screen.blit(self.txt_title2, (self.title_pos[0] + offset_x - self.txt_title2.get_width()//2, self.title_pos[1] + 25))
        self.screen.blit(c_surf, (self.count_pos[0] + offset_x - c_surf.get_width()//2, self.count_pos[1] - c_surf.get_height()//2))

        if alpha > 0:
            mult = reborn_system.get_multiplier()
            click_surf = self.stats_font.render(f"{int(stats.click_power * mult)}/click", True, (108, 73, 58))
            sec_surf = self.stats_font.render(f"{int(stats.auto_click_rate * mult)}/sec", True, (108, 73, 58))
            
            for s in [click_surf, sec_surf, self.icon_click, self.icon_sec]: 
                s.set_alpha(alpha)
            
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

            upgrades_manager.draw(self.screen, offset_x, stats.clicks, alpha)

        shake = random.randint(-4, 4) if stats.egg_is_pressed else 0
        img = self.egg_pressed_image if stats.egg_is_pressed else self.egg_image
        if img:
            img.set_alpha(alpha)
            self.screen.blit(img, img.get_rect(center=(self.egg_pos[0] + offset_x + shake, self.egg_pos[1] + shake)))

    def draw_custom_scene(self, offset_x, alpha, skin_manager):
        self.shop_background.set_alpha(alpha)
        self.screen.blit(self.shop_background, (offset_x, 0))
        skin_manager.draw(self.screen, offset_x, alpha)

    def draw(self, bg, state_manager, stats, reborn_system, skin_manager, upgrades_manager, cursor):
        bg.draw(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        
        if state_manager.game_state == "menu":
            self.screen.blit(self.logo, self.logo_rect)
            for btn in [self.btn_start, self.btn_custom, self.btn_exit, self.btn_sound, self.btn_reborn]: 
                btn.draw(self.screen)
            
            if state_manager.show_reborn_window:
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (0, 0))
                self.screen.blit(self.reborn_window_surf, self.reborn_window_rect)
                self.screen.blit(self.close_txt_surf, self.close_txt_rect)

                cy = self.screen_height // 2
                win_top, win_bottom = cy - int(self.screen_height * 0.40), cy + int(self.screen_height * 0.40)

                texts = [
                    (self.reborn_title_font.render("REBORN", True, (108, 73, 58)), win_top),
                    (self.reborn_main_font.render(f"number of reborns: {reborn_system.count}", True, (108, 73, 58)), win_top + 130),
                    (self.reborn_sub_font.render("Rebirths completely reset progress", True, (143, 99, 79)), cy - 80),
                    (self.reborn_sub_font.render(f"Cost: {reborn_system.get_cost()} clicks", True, (143, 99, 79)), cy),
                    (self.reborn_sub_font.render(f"Reward: x{reborn_system.get_multiplier() + 1} multiplier", True, (143, 99, 79)), cy + 80)
                ]
                
                for txt, y_pos in texts:
                    self.screen.blit(txt, (self.screen_width//2 - txt.get_width()//2, y_pos))

                can_reborn = reborn_system.can_reborn(stats.clicks)
                btn_color = (96, 192, 96) if can_reborn else (255, 105, 97)
                t_btn = self.reborn_title_font.render("Reborn now" if can_reborn else "Not enough clicks!", True, btn_color)
                
                btn_w, btn_h = max(t_btn.get_width() + 100, 400), t_btn.get_height() + 40
                self.btn_confirm_reborn_rect.size = (btn_w, btn_h)
                self.btn_confirm_reborn_rect.center = (self.screen_width // 2, win_bottom - 80)
                
                self.screen.blit(pygame.transform.scale(self.empty_btn_img, (btn_w, btn_h)), self.btn_confirm_reborn_rect.topleft)
                self.screen.blit(t_btn, t_btn.get_rect(center=self.btn_confirm_reborn_rect.center))
            
        elif "transition" in state_manager.game_state:
            if state_manager.menu_offset > 0 or state_manager.game_state == "transition": 
                self.draw_game_scene(state_manager.overlay_offset, state_manager.global_alpha, stats, reborn_system, upgrades_manager)
            elif state_manager.menu_offset < 0 or state_manager.game_state == "transition_custom": 
                self.draw_custom_scene(state_manager.custom_overlay_offset, state_manager.global_alpha, skin_manager)
            
            l_rect = self.logo_rect.copy()
            l_rect.x += state_manager.menu_offset
            self.screen.blit(self.logo, l_rect)

            for btn in [self.btn_start, self.btn_custom, self.btn_exit, self.btn_sound, self.btn_reborn]: 
                old_x = btn.rect.x
                btn.rect.x += state_manager.menu_offset
                btn.draw(self.screen)
                btn.rect.x = old_x
            
        elif state_manager.game_state == "game": 
            self.draw_game_scene(0, 255, stats, reborn_system, upgrades_manager)
        elif state_manager.game_state == "custom": 
            self.draw_custom_scene(0, 255, skin_manager)

        cursor.draw(self.screen)
        pygame.display.flip()

    def update_buttons(self, state_manager, allow_interaction):
        mouse_pos = pygame.mouse.get_pos()
        if allow_interaction and ("transition" in state_manager.game_state or state_manager.game_state == "menu"):
            if not state_manager.show_reborn_window:
                for btn in [self.btn_start, self.btn_custom, self.btn_exit, self.btn_sound, self.btn_reborn]:
                    btn.update(mouse_pos)