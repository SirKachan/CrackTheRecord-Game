import pygame

class CursorManager:
    def __init__(self, image_path='textures/cursor.png', size=None):
        self.surface = pygame.image.load(image_path).convert_alpha()
        if size:
            self.surface = pygame.transform.scale(self.surface, size)

        self.visible = True
        pygame.mouse.set_visible(False)

    def enable(self):
        pygame.mouse.set_visible(False)
        self.visible = True

    def disable(self):
        pygame.mouse.set_visible(True)
        self.visible = False

    def draw(self, screen):
        if self.visible:
            rect = self.surface.get_rect(center=pygame.mouse.get_pos())
            screen.blit(self.surface, rect)