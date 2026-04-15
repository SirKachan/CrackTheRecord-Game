import pygame
from src.core.config import EGG_PRESS_DURATION

class EventHandler:
    def __init__(self, audio, state_manager, renderer, stats, reborn_system, skin_manager, upgrades_manager):
        self.audio = audio
        self.state_manager = state_manager
        self.renderer = renderer
        self.stats = stats
        self.reborn_system = reborn_system
        self.skin_manager = skin_manager
        self.upgrades_manager = upgrades_manager

    def handle_events(self):
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state_manager.is_exiting = True
                self.state_manager.exit_timer = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state_manager.show_reborn_window: 
                    self.state_manager.show_reborn_window = False
                elif self.state_manager.game_state == "game": 
                    self.state_manager.game_state = "transition_back"
                elif self.state_manager.game_state == "custom": 
                    self.state_manager.game_state = "transition_custom_back"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        mouse_pos = pygame.mouse.get_pos()

        if self.state_manager.show_reborn_window:
            if mouse_clicked:
                if self.renderer.close_txt_rect.collidepoint(mouse_pos):
                    self.audio.play_sound('click')
                    self.state_manager.show_reborn_window = False
                elif self.renderer.btn_confirm_reborn_rect.collidepoint(mouse_pos) and self.reborn_system.can_reborn(self.stats.clicks):
                    self.audio.play_sound('buy')
                    self.reborn_system.do_reborn()
                    
                    # Reset stats
                    self.stats.reset()
                    self.upgrades_manager.setup_upgrades(self.renderer.screen_width, self.renderer.screen_height)
                    self.upgrades_manager.check_upgrades_unlock(self.stats.total_clicks)

                    self.state_manager.show_reborn_window = False
            return 

        if self.state_manager.game_state == "menu" and not self.state_manager.is_exiting:
            button_clicked = True 
            if self.renderer.btn_exit.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.state_manager.is_exiting = True
                self.state_manager.exit_timer = 300 
            elif self.renderer.btn_custom.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.state_manager.game_state = "transition_custom"
            elif self.renderer.btn_start.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.state_manager.game_state = "transition" 
            elif self.renderer.btn_sound.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                is_on = not self.audio.is_music_on
                self.audio.set_music_state(is_on)
                self.renderer.update_sound_button_icon(is_on)
            elif self.renderer.btn_reborn.is_clicked(mouse_pos, mouse_clicked):
                self.audio.play_sound('click')
                self.state_manager.show_reborn_window = True
            else:
                button_clicked = False

            if mouse_clicked and self.renderer.logo_rect.collidepoint(mouse_pos) and not button_clicked:
                self.audio.play_sound('kukareku') 
        
        elif self.state_manager.game_state == "game" and mouse_clicked:
            egg_rect = self.renderer.egg_image.get_rect(center=self.renderer.egg_pos)
            if egg_rect.collidepoint(mouse_pos):
                current_time = pygame.time.get_ticks()
                time_since_last = current_time - self.stats.last_click_time
                self.stats.last_click_time = current_time 
                
                if time_since_last >= 40:
                    self.audio.play_sound('egg_click')
                    actual_power = self.stats.click_power * self.reborn_system.get_multiplier()
                    self.stats.clicks += actual_power
                    self.stats.total_clicks += actual_power
                    self.stats.egg_is_pressed = True
                    self.stats.egg_press_timer = EGG_PRESS_DURATION
                    self.upgrades_manager.check_upgrades_unlock(self.stats.total_clicks)
            else:
                self.upgrades_manager.handle_purchases(mouse_pos, self.stats, self.audio)
                    
        elif self.state_manager.game_state == "custom" and mouse_clicked:
            self.skin_manager.handle_click(mouse_pos)