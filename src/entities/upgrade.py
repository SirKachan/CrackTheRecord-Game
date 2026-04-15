import pygame

class Upgrade:
    def __init__(self, name, base_price, price_growth, icon_path, effect_type, effect_value, position, size, unlock_condition):
        self.name = name
        self.base_price = base_price
        self.price_growth = price_growth
        self.level = 0
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.unlock_condition = unlock_condition
        self.is_unlocked = False

        self.icon = pygame.transform.scale(pygame.image.load(icon_path).convert_alpha(), size)
        self.unknown_icon = pygame.transform.scale(pygame.image.load('textures/upgrades/unknown.png').convert_alpha(), size)
        self.font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 36)

        self.rect = pygame.Rect(*position, *size)
        self.hovered = False
        
    def check_unlock(self, total_clicks):
        if not self.is_unlocked:
            self.is_unlocked = total_clicks >= self.unlock_condition
        return self.is_unlocked
    
    def get_price(self):
        return int(self.base_price * (self.price_growth ** self.level))
    
    def purchase(self):
        self.level += 1
        return self.effect_value
    
    def draw(self, screen, offset_x=0, can_afford=False, alpha=255):
        if alpha <= 0: 
            return
            
        draw_rect = self.rect.copy()
        draw_rect.x += offset_x
        
        icon_to_draw = self.icon if self.is_unlocked else self.unknown_icon
        
        if alpha < 255:
            icon_copy = icon_to_draw.copy()
            icon_copy.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(icon_copy, draw_rect)
        else:
            screen.blit(icon_to_draw, draw_rect)
            
        if self.hovered and self.is_unlocked and can_afford and alpha == 255:
            highlight = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 30))
            screen.blit(highlight, draw_rect)
        
        if self.is_unlocked:
            level_surface = self.font.render(f"LVL {self.level}", True, (136, 114, 88))
            price_color = (96, 192, 96) if can_afford else (255, 105, 97)
            price_surface = self.font.render(str(self.get_price()), True, price_color)
            
            if alpha < 255:
                level_surface.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                price_surface.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
            
            level_x = draw_rect.right - level_surface.get_width() - 30
            level_y = draw_rect.top + 20
            price_x = draw_rect.right - price_surface.get_width() - 30
            price_y = draw_rect.bottom - price_surface.get_height() - 20
            
            screen.blit(level_surface, (level_x, level_y))
            screen.blit(price_surface, (price_x, price_y))