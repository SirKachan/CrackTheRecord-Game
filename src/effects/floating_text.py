import pygame
import random

class FloatingText:
    def __init__(self, x, y, value, color=(220, 220, 220), duration=800, speed_y=-120):
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.duration = duration
        self.max_duration = duration
        self.speed_y = speed_y
        self.font = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', 36)
        self.x += random.randint(-50, 50)
        self.y += random.randint(-40, 40)

    def update(self, dt_seconds):
        self.duration -= dt_seconds * 1000
        if self.duration <= 0:
            return False
        self.y += self.speed_y * dt_seconds
        return True

    def draw(self, screen, camera_offset=0):
        alpha = int(255 * (self.duration / self.max_duration))
        if alpha <= 0:
            return
        text = f"+{int(self.value)}"
        surf = self.font.render(text, True, self.color)
        surf.set_alpha(alpha)
        screen.blit(surf, (self.x + camera_offset - surf.get_width()//2, self.y - surf.get_height()//2))


class FloatingTextManager:
    def __init__(self):
        self.texts = []

    def add_text(self, x, y, value, color=(220, 220, 220)):
        self.texts.append(FloatingText(x, y, value, color))

    def update(self, dt_seconds):
        self.texts = [t for t in self.texts if t.update(dt_seconds)]

    def draw(self, screen, camera_offset=0):
        for t in self.texts:
            t.draw(screen, camera_offset)

    def clear(self):
        self.texts.clear()