import pygame

class Button:
    def __init__(self, normal_img_path, shadow_img_path, position, size, center=True, hover_sound=None):
        normal_img = pygame.image.load(normal_img_path).convert_alpha()
        shadow_img = pygame.image.load(shadow_img_path).convert_alpha()

        self.normal_image = pygame.transform.scale(normal_img, size)
        self.shadow_image = pygame.transform.scale(shadow_img, size)
        if center:
            self.rect = self.normal_image.get_rect(center=position)
        else:
            self.rect = self.normal_image.get_rect(topleft=position)

        self.current_image = self.normal_image
        self.is_hovered = False
        self.was_hovered = False
        self.hover_sound = hover_sound

    def update(self, mouse_pos):
        self.was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.current_image = self.shadow_image
            if not self.was_hovered and self.hover_sound:
                self.hover_sound.play()
        else:
            self.current_image = self.normal_image

    def draw(self, screen):
        screen.blit(self.current_image, self.rect)

    def is_clicked(self, mouse_pos, mouse_clicked):
        return mouse_clicked and self.rect.collidepoint(mouse_pos)