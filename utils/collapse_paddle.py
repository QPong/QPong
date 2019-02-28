import pygame
from utils.colors import *

class Collapse(pygame.sprite.Sprite):
    def __init__(self, qubit_num):
        super().__init__()

        self.image = pygame.Surface([10, 500/2**qubit_num])
        self.image.fill((255,0,255, 0))

        #self.image.blit()

        self.rect = self.image.get_rect()

        self.screenheight = 500

        self.x = 1000
        self.y = 0

        self.update()

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def position(self, qubit_num, measurement):
        # self.image.fill(WHITE)
        self.image.fill((255,0,255, 1))

        self.y = self.screenheight*measurement / 2**qubit_num
        self.update()

    def comp_position(self, qubit_num, measurement):
        self.image.fill(WHITE)

        self.x = 0
        self.y = self.screenheight*measurement / qubit_num
        self.update()

    def reset(self):
        self.image.fill((WHITE, 0))

        self.y = 0
