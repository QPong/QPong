import pygame
from utils.colors import *

class Collapse(pygame.sprite.Sprite):
    def __init__(self, qubit_num):
        super().__init__()

        self.image = pygame.Surface([20, 500/qubit_num])
        self.image.fill((255,255,255, 0))

        self.rect = self.image.get_rect()

        self.screenheight = 500

        self.x = 1000
        self.y = 0

    def position(self, qubit_num, measurement):
        # self.image.fill(WHITE)
        self.image.fill(BLACK)

        self.y = self.screenheight*measurement / qubit_num

    def comp_position(self, qubit_num, measurement):
        self.image.fill(WHITE)

        self.x = 0
        self.y = self.screenheight*measurement / qubit_num

    def reset(self):
        self.image.fill(WHITE, 0)

        self.y = 0
