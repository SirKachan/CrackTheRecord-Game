import pygame

class Achievement:
    def __init__(self, id, name, description, icon_unlocked_path, icon_locked_path, condition):
        self.id = id
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = False

        self.icon_unlocked = pygame.image.load(icon_unlocked_path).convert_alpha()
        self.icon_locked = pygame.image.load(icon_locked_path).convert_alpha()

    @property
    def image(self):
        return self.icon_unlocked if self.unlocked else self.icon_locked

    def check(self, context):
        if not self.unlocked and self.condition(context):
            self.unlocked = True
        return self.unlocked
