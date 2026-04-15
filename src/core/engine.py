import pygame
import sys

from src.core.config import FPS, TRANSITION_SPEED
from src.core.audio import Audio
from src.ui.background import Background
from src.ui.cursor_manager import CursorManager
from src.systems.storage import GameStorage
from src.systems.reborn import RebornSystem
from src.ui.skins import SkinManager
from src.entities.player_stats import PlayerStats
from src.core.state_manager import StateManager
from src.systems.upgrades_manager import UpgradesManager
from src.ui.renderer import Renderer
from src.core.event_handler import EventHandler

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Crack the Record!")
        
        screen_width, screen_height = self.screen.get_size()

        self.cursor_manager = CursorManager('textures/cursor.png', size=(64, 64))
        self.cursor_manager.enable()

        self.audio = Audio()
        self.audio.load_sounds()
        
        self.background = Background(screen_width, screen_height)
        self.storage = GameStorage()
        self.reborn_system = RebornSystem() 
        self.skin_manager = SkinManager(self)
        
        self.stats = PlayerStats()
        self.state_manager = StateManager(screen_width)
        
        self.renderer = Renderer(self.screen, self.audio)
        self.upgrades_manager = UpgradesManager(screen_width, screen_height)
        
        self.event_handler = EventHandler(
            self.audio, self.state_manager, self.renderer, 
            self.stats, self.reborn_system, self.skin_manager, self.upgrades_manager
        )

        self.load_game_data()
        self.audio.load_background_music() 
        
        self.clock = pygame.time.Clock()

    def apply_skin(self, filename):
        self.renderer.apply_skin(filename)

    def load_game_data(self):
        data = self.storage.load()
        self.stats.clicks = data.get('clicks', 0)
        self.stats.total_clicks = data.get('total_clicks', 0)
        self.stats.click_power = data.get('click_power', 1)
        self.stats.auto_click_rate = data.get('auto_click_rate', 0)
        
        self.reborn_system.count = data.get('reborn_count', 0)
        
        self.skin_manager.unlocked_ids = data.get('unlocked_skins', ['default'])
        self.skin_manager.active_id = data.get('active_skin', 'default')
        
        active_skin = next((s for s in self.skin_manager.skins if s['id'] == self.skin_manager.active_id), self.skin_manager.skins[0])
        self.apply_skin(active_skin['filename'])
        
        is_music_on = data.get('music_on', True)
        self.audio.set_music_state(is_music_on)
        self.renderer.update_sound_button_icon(is_music_on)
        
        upgrades_data = data.get('upgrades', {})
        for u in self.upgrades_manager.upgrades:
            if u.name in upgrades_data:
                u.level = upgrades_data[u.name].get('level', 0)
                u.is_unlocked = upgrades_data[u.name].get('is_unlocked', False)
            u.check_unlock(self.stats.total_clicks)

    def save_game_data(self):
        data = {
            'clicks': self.stats.clicks,
            'total_clicks': self.stats.total_clicks,
            'click_power': self.stats.click_power,
            'auto_click_rate': self.stats.auto_click_rate,
            'reborn_count': self.reborn_system.count, 
            'music_on': self.audio.is_music_on,
            'unlocked_skins': self.skin_manager.unlocked_ids, 
            'active_skin': self.skin_manager.active_id,       
            'upgrades': {u.name: {'level': u.level, 'is_unlocked': u.is_unlocked} for u in self.upgrades_manager.upgrades}
        }
        self.storage.save(data)

    def update(self, dt):
        self.background.update()
        
        if self.stats.egg_is_pressed:
            self.stats.egg_press_timer -= dt
            if self.stats.egg_press_timer <= 0:
                self.stats.egg_is_pressed = False

        self.state_manager.update(dt, TRANSITION_SPEED)
        self.renderer.update_buttons(self.state_manager, allow_interaction=True)

        if self.state_manager.game_state in ["transition", "transition_back", "game"]:
            mouse_pos = pygame.mouse.get_pos()
            self.upgrades_manager.update_hover(mouse_pos)
                
            if self.state_manager.game_state == "game":
                self.stats.auto_click_timer += dt
                if self.stats.auto_click_timer >= 1000:
                    self.stats.auto_click_timer -= 1000
                    if self.stats.auto_click_rate > 0:
                        actual_rate = self.stats.auto_click_rate * self.reborn_system.get_multiplier()
                        self.stats.clicks += actual_rate
                        self.stats.total_clicks += actual_rate
                        self.upgrades_manager.check_upgrades_unlock(self.stats.total_clicks)

    def draw(self):
        self.renderer.draw(
            self.background,
            self.state_manager,
            self.stats,
            self.reborn_system,
            self.skin_manager,
            self.upgrades_manager,
            self.cursor_manager
        )

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) 
            self.event_handler.handle_events()
            
            if self.state_manager.should_quit():
                running = False
            
            self.update(dt)
            self.draw()
            
        self.save_game_data()
        pygame.quit()
        sys.exit()