import pygame

SKINS_CONFIG = [
    {'id': 'default', 'name': 'Classic Egg', 'filename': 'textures/egg.png', 'cost_clicks': 0, 'cost_reborns': 0},
    {'id': 'striped', 'name': 'Striped Egg', 'filename': 'textures/skins/striped_egg.png', 'cost_clicks': 500, 'cost_reborns': 0},
    {'id': 'silver', 'name': 'Silver Egg', 'filename': 'textures/skins/silver_egg.png', 'cost_clicks': 2500, 'cost_reborns': 0},
    {'id': 'gold', 'name': 'Gold Egg', 'filename': 'textures/skins/gold_egg.png', 'cost_clicks': 10000, 'cost_reborns': 0},
    {'id': 'cosmic', 'name': 'Cosmic Egg', 'filename': 'textures/skins/cosmic_egg.png', 'cost_clicks': 50000, 'cost_reborns': 1},
    {'id': 'leopard', 'name': 'Leopard Egg', 'filename': 'textures/skins/leopard_egg.png', 'cost_clicks': 100000, 'cost_reborns': 2},
    {'id': 'technology', 'name': 'Tech Egg', 'filename': 'textures/skins/technology_egg.png', 'cost_clicks': 250000, 'cost_reborns': 5},
]

class SkinManager:
    def __init__(self, game):
        self.game = game
        self.skins = []
        self.unlocked_ids = ['default']
        self.active_id = 'default'
        
        self.title_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 72)
        self.price_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 48)
        self.btn_font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 56)

        self.load_textures()
        self.selected_skin = self.skins[0]
        
        self.rects = {} 
        self.btn_rect = None 

    def load_textures(self):
        for conf in SKINS_CONFIG:
            img = pygame.image.load(conf['filename']).convert_alpha()
            self.skins.append({**conf, 'original_img': img})
            
        self.empty_btn_img = pygame.image.load('textures/button_empty.png').convert_alpha()

    def draw(self, screen, offset_x, alpha):
        w, h = self.game.screen.get_size()
        start_cx, start_cy = offset_x + w * 0.625, h * 0.25              
        step_x, step_y = w * 0.128, h * 0.26   
        max_icon_w, max_icon_h = w * 0.11, h * 0.23  
        
        for i, skin in enumerate(self.skins):
            cx = start_cx + (i % 3) * step_x
            cy = start_cy + (i // 3) * step_y
            
            img = skin['original_img']
            scale = min(max_icon_w / img.get_width(), max_icon_h / img.get_height())
            tw, th = int(img.get_width() * scale), int(img.get_height() * scale)
            
            thumb = pygame.transform.scale(img, (tw, th))
            thumb.set_alpha(alpha)
            
            rect = thumb.get_rect(center=(cx, cy))
            screen.blit(thumb, rect)
            self.rects[skin['id']] = rect

        left_cx = offset_x + w * 0.25
        name_txt = self.title_font.render(self.selected_skin['name'], True, (108, 73, 58))
        name_txt.set_alpha(alpha)
        screen.blit(name_txt, name_txt.get_rect(center=(left_cx, h * 0.15)))

        sel_img = self.selected_skin['original_img']
        scale_l = min((w * 0.25) / sel_img.get_width(), (h * 0.4) / sel_img.get_height())
        lw, lh = int(sel_img.get_width() * scale_l), int(sel_img.get_height() * scale_l)
        
        large_img = pygame.transform.scale(sel_img, (lw, lh))
        large_img.set_alpha(alpha)
        screen.blit(large_img, large_img.get_rect(center=(left_cx, h * 0.45)))
        
        is_unlocked = self.selected_skin['id'] in self.unlocked_ids
        
        if not is_unlocked:
            costs = []
            if self.selected_skin['cost_clicks'] > 0:
                costs.append(f"{self.selected_skin['cost_clicks']} Clicks")
            if self.selected_skin['cost_reborns'] > 0:
                costs.append(f"{self.selected_skin['cost_reborns']} Reborns")
            price_str = " + ".join(costs)
        else:
            price_str = "Unlocked"
            
        price_txt = self.price_font.render(price_str, True, (143, 99, 79))
        price_txt.set_alpha(alpha)
        screen.blit(price_txt, price_txt.get_rect(center=(left_cx, h * 0.72)))
        
        can_buy = (self.game.stats.clicks >= self.selected_skin['cost_clicks'] and 
                   self.game.reborn_system.count >= self.selected_skin['cost_reborns'])
        
        if self.active_id == self.selected_skin['id']:
            btn_str, btn_color = "Equipped", (150, 150, 150)
        elif is_unlocked:
            btn_str, btn_color = "Equip", (96, 192, 96)
        elif can_buy:
            btn_str, btn_color = "Buy", (96, 192, 96)
        else:
            btn_str, btn_color = "Not enough", (255, 105, 97)
            
        btn_txt = self.btn_font.render(btn_str, True, btn_color)
        btn_txt.set_alpha(alpha)
        
        bg_w, bg_h = max(btn_txt.get_width() + 80, 300), btn_txt.get_height() + 40
        self.btn_rect = pygame.Rect(0, 0, bg_w, bg_h)
        self.btn_rect.center = (left_cx, h * 0.85)
        
        bg_img = pygame.transform.scale(self.empty_btn_img, (bg_w, bg_h))
        bg_img.set_alpha(alpha)
        
        screen.blit(bg_img, self.btn_rect.topleft)
        screen.blit(btn_txt, btn_txt.get_rect(center=self.btn_rect.center))

    def handle_click(self, mouse_pos):
        for skin_id, rect in self.rects.items():
            if rect.collidepoint(mouse_pos):
                self.game.audio.play_sound('click')
                self.selected_skin = next(s for s in self.skins if s['id'] == skin_id)
                return
        
        if self.btn_rect and self.btn_rect.collidepoint(mouse_pos):
            if self.active_id == self.selected_skin['id']:
                return 
                
            is_unlocked = self.selected_skin['id'] in self.unlocked_ids
            can_buy = (self.game.stats.clicks >= self.selected_skin['cost_clicks'] and 
                       self.game.reborn_system.count >= self.selected_skin['cost_reborns'])
            
            if is_unlocked or can_buy:
                if not is_unlocked:
                    self.game.audio.play_sound('buy')
                    self.game.stats.clicks -= self.selected_skin['cost_clicks'] 
                    self.unlocked_ids.append(self.selected_skin['id'])
                else:
                    self.game.audio.play_sound('click')
                    
                self.active_id = self.selected_skin['id']
                self.game.apply_skin(self.selected_skin['filename'])