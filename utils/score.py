import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player = 0
        self.computer = 0

    def update(self, score):
        if score == 1:
            self.player += 1

        if score == 2:
            self.computer += 1
