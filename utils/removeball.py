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

class RemoveBall(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        super().__init__()

        self.image = pygame.Surface([10, 10])

        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        self.screenheight = 500
        self.screenwidth = 1000

        self.RIGHT_EDGE = self.screenwidth + LEFT_EDGE

        self.height = 10
        self.width = 10

        self.x = xpos
        self.y = ypos
        self.speed = 0
        self.direction = 0

    def update(self, xpos, ypos):
        radians = math.radians(self.direction)

        self.x = xpos
        self.y = ypos

        # Update ball position
        self.rect.x = self.x
        self.rect.y = self.y


