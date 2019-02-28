import pygame
import math
import random
import numpy as np
from utils.colors import *
from utils.navigation import *
from utils.resources import *
from model.circuit_grid_model import CircuitGridNode
from model import circuit_node_types as node_types

LEFT_EDGE=100
TOP_EDGE=0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([10, 10])

        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

        self.screenheight = 500
        self.screenwidth = 1000

        self.height = 10
        self.width = 10

        self.x = 0
        self.y = 0
        self.speed = 0
        self.direction = 0

        self.ball_reset()

    def update(self):
        radians = math.radians(self.direction)

        self.x += self.speed * math.sin(radians)
        self.y -= self.speed * math.cos(radians)

        if self.x < LEFT_EDGE:
            self.ball_reset()
        if self.x > self.screenwidth:
            self.ball_reset()

        # Update ball position
        self.rect.x = self.x
        self.rect.y = self.y

        if self.y <= TOP_EDGE:
            self.direction = (180-self.direction) % 360
        if self.y > self.screenheight - self.height:
            self.direction = (180-self.direction) % 360

    def ball_reset(self):
        self.x = LEFT_EDGE+50
        self.y = self.screenheight/2

        self.speed = 8.0
        self.direction = random.randrange(0, 90)

    def bounce_vert(self, diff):
        self.direction = (360-self.direction) % 360
        self.direction -= diff

    def check_score(self):
        if self.x < LEFT_EDGE:
            return 1
        if self.x > self.screenwidth:
            return 2
        else:
            return 0
