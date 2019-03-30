import pygame
import math
import random
import numpy as np
from utils.colors import *
from utils.navigation import *
from utils.resources import *
from model.circuit_grid_model import CircuitGridNode
from model import circuit_node_types as node_types

LEFT_EDGE=50
TOP_EDGE=0

MEASURE_RIGHT = 1
BOUNCE_RIGHT = 2
MEASURE_LEFT = 3
BOUNCE_LEFT = 4
NOTHING = 0

YES = 1
NO = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([10, 10])

        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

        self.screenheight = 500
        self.screenwidth = 1000

        self.LEFT_EDGE = LEFT_EDGE
        self.RIGHT_EDGE = self.screenwidth + self.LEFT_EDGE

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

        #if self.x < LEFT_EDGE:
        #    self.ball_reset()
        #if self.x > self.RIGHT_EDGE:
        #    self.ball_reset()

        # Update ball position
        self.rect.x = self.x
        self.rect.y = self.y

        if self.y <= TOP_EDGE + self.height:
            self.direction = (180-self.direction) % 360
        if self.y > self.screenheight - 2*self.height:
            self.direction = (180-self.direction) % 360

    def ball_reset(self):
        self.x = LEFT_EDGE+random.randint(100,200)
        self.y = self.screenheight/2

        self.speed = 8.0
        self.direction = random.randrange(30, 60)

    def bounce_edge(self):
        self.direction = (360-self.direction) % 360

        self.speed *= 1.1

    def get_xpos(self):
        xpos = self.x
        return xpos

    def get_ypos(self):
        ypos = self.y
        return ypos

    # 1 = comp, 2 = player, none = 0
    def action(self, ball_action, measure_flag, bounce_flag):

        if self.RIGHT_EDGE-30 < self.x < self.RIGHT_EDGE-15:
            if measure_flag == NO:
                # do measurement if not yet done
                print("measure right")
                ball_action = MEASURE_RIGHT
                measure_flag = YES
            else:
                # do nothing if measurement was done already
                ball_action = NOTHING
        elif self.RIGHT_EDGE > self.x > self.RIGHT_EDGE-15:
            if bounce_flag == NO:
                # trigger bounce edge if noe yet done
                print ("bounce right")
                ball_action = BOUNCE_RIGHT
                bounce_flag = YES
            else:
                # do nothing if measurement was done already
                ball_action = NOTHING
        elif self.LEFT_EDGE+30 >self.x > self.LEFT_EDGE+15:
            if measure_flag == NO:
                print ("measure left")
                ball_action = MEASURE_LEFT
                measure_flag = YES
            else:
                ball_action = NOTHING
        elif self.LEFT_EDGE < self.x < self.LEFT_EDGE+15:
            if bounce_flag == NO:
                print ("bounce left")
                ball_action = BOUNCE_LEFT
                measure_flag = NO
            else:
                ball_action = NOTHING
        elif self.x < self.LEFT_EDGE:
            self.ball_reset()
        elif self.x > self.RIGHT_EDGE:
            self.ball_reset()
        else:
            # reset flags and do nothing when the ball is outside measurement and bounce region
            ball_action = NOTHING
            measure_flag = NO
            bounce_flag = NO

        return ball_action, measure_flag, bounce_flag


    def check_score(self):
        if self.x < LEFT_EDGE:
            return 1
        if self.x > self.RIGHT_EDGE:
            return 2
        else:
            return 0
