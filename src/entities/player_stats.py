class PlayerStats:
    def __init__(self):
        self.clicks = 0
        self.total_clicks = 0
        self.click_power = 1
        self.auto_click_rate = 0
        self.auto_click_timer = 0
        self.last_click_time = 0
        
        self.egg_is_pressed = False
        self.egg_press_timer = 0

    def reset(self):
        self.clicks = 0
        self.total_clicks = 0
        self.click_power = 1
        self.auto_click_rate = 0
        self.auto_click_timer = 0
        self.last_click_time = 0
        self.egg_is_pressed = False
        self.egg_press_timer = 0