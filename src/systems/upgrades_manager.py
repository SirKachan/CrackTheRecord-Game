import pygame
from src.entities.upgrade import Upgrade
from src.core.config import UPGRADES_CONFIG

class UpgradesManager:
    def __init__(self, screen_width, screen_height):
        self.upgrades = []
        self.setup_upgrades(screen_width, screen_height)

    def setup_upgrades(self, screen_width, screen_height):
        icon_width, icon_height, spacing = 632, 144, 160 
        start_x = screen_width * 3 // 4 - icon_width // 2 + 30
        start_y = screen_height // 2 - 280
        
        self.upgrades = [
            Upgrade(d['name'], d['base_price'], d['price_growth'], d['icon'], d['effect_type'], d['effect_value'],
                    (start_x, start_y + i * spacing), (icon_width, icon_height), d['unlock_condition'])
            for i, d in enumerate(UPGRADES_CONFIG)
        ]

    def check_upgrades_unlock(self, total_clicks):
        for u in self.upgrades: 
            u.check_unlock(total_clicks)

    def update_hover(self, mouse_pos):
        for u in self.upgrades:
            u.hovered = u.rect.collidepoint(mouse_pos)

    def handle_purchases(self, mouse_pos, stats, audio):
        for u in self.upgrades:
            if u.rect.collidepoint(mouse_pos) and u.is_unlocked and stats.clicks >= u.get_price():
                stats.clicks -= u.get_price()
                u.purchase()
                audio.play_sound('buy') 
                
                if u.effect_type == 'click': 
                    stats.click_power += u.effect_value
                elif u.effect_type == 'auto': 
                    stats.auto_click_rate += u.effect_value
                self.check_upgrades_unlock(stats.total_clicks)

    def draw(self, screen, offset_x, clicks, alpha):
        for u in self.upgrades:
            u.draw(screen, offset_x, clicks >= u.get_price(), alpha)