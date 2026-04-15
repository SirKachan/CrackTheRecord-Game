class StateManager:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.game_state = "menu"
        self.menu_offset = 0
        self.overlay_offset = -screen_width
        self.custom_overlay_offset = screen_width
        self.global_alpha = 0
        self.show_reborn_window = False
        self.is_exiting = False
        self.exit_timer = 0
        
    def update(self, dt, transition_speed):
        if self.is_exiting:
            self.exit_timer -= dt

        if self.game_state == "transition":
            self.menu_offset = min(self.screen_width, self.menu_offset + transition_speed * (dt / 16))
            if self.menu_offset >= self.screen_width:
                self.game_state = "game"
        elif self.game_state == "transition_back":
            self.menu_offset = max(0, self.menu_offset - transition_speed * (dt / 16))
            if self.menu_offset <= 0:
                self.game_state = "menu"
        elif self.game_state == "transition_custom":
            self.menu_offset = max(-self.screen_width, self.menu_offset - transition_speed * (dt / 16))
            if self.menu_offset <= -self.screen_width:
                self.game_state = "custom"
        elif self.game_state == "transition_custom_back":
            self.menu_offset = min(0, self.menu_offset + transition_speed * (dt / 16))
            if self.menu_offset >= 0:
                self.game_state = "menu"

        self.overlay_offset = -self.screen_width + self.menu_offset
        self.custom_overlay_offset = self.screen_width + self.menu_offset
        self.global_alpha = int(255 * (abs(self.menu_offset) / self.screen_width))

    def should_quit(self):
        return self.is_exiting and self.exit_timer <= 0