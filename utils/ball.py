import pygame
import math
import random
import numpy as np
from utils.colors import *
from utils.navigation import *
from utils.resources import *
from utils.sound import *
from utils.score import *
from model.circuit_grid_model import CircuitGridNode
from model import circuit_node_types as node_types

LEFT_EDGE=10
TOP_EDGE=0

LEFT = 0
RIGHT = 1

MEASURE_RIGHT = 1
MEASURE_LEFT = 2
NOTHING = 0

YES = 1
NO = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([10, 10])

        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

        self.screenheight = 520
        self.screenwidth = 1200

        self.LEFT_EDGE = LEFT_EDGE
        self.RIGHT_EDGE = self.screenwidth - self.LEFT_EDGE

        self.height = 10
        self.width = 10

        self.x = 0
        self.y = 0
        self.speed = 0
        self.direction = 0

        # initialize ball action type, measure and bounce flags
        self.ball_action = NOTHING
        self.measure_flag = NO

        # initialize ball reset on the left
        self.reset_position = LEFT
        self.ball_reset()

        self.sound = Sound()
        self.score = Score()

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
            self.sound.edge_sound()
        if self.y > self.screenheight - 2*self.height:
            self.direction = (180-self.direction) % 360
            self.sound.edge_sound()

    def ball_reset(self):

        self.y = self.screenheight / 2
        self.speed = 8.0

        # alternate reset at left and right
        if self.reset_position == LEFT:
            self.x = self.LEFT_EDGE+100
            self.direction = random.randrange(30, 120)
            self.reset_position = RIGHT
        else:
            self.x = self.RIGHT_EDGE-200
            self.direction = random.randrange(-120, -30)
            self.reset_position = LEFT

    def bounce_edge(self):
        self.direction = (360-self.direction) % 360
        self.speed *= 1.1
        self.sound.bounce_sound()

    def get_xpos(self):
        xpos = self.x
        return xpos

    def get_ypos(self):
        ypos = self.y
        return ypos

    # 1 = comp, 2 = player, none = 0
    def action(self):

        if self.x < self.LEFT_EDGE:
            # reset the ball when it reaches beyond left edge
            self.ball_reset()
            self.sound.lost_sound()
            self.score.update(1)

        elif self.LEFT_EDGE + 15 <= self.x < self.LEFT_EDGE + 50:
            # measure the ball when it reaches the left measurement zone
            if self.measure_flag == NO:
                print("measure left")
                self.ball_action = MEASURE_LEFT
                self.measure_flag = YES
            else:
                self.ball_action = NOTHING

        elif self.RIGHT_EDGE - 150 <= self.x < self.RIGHT_EDGE - 120:
            # measure the ball when it reaches the right measurement zone
            if self.measure_flag == NO:
                # do measurement if not yet done
                print("measure right")
                self.ball_action = MEASURE_RIGHT
                self.measure_flag = YES
            else:
                # do nothing if measurement was done already
                self.ball_action = NOTHING

        elif self.x > self.RIGHT_EDGE:
            # reset the ball when it reaches beyond right edge
            self.ball_reset()
            self.sound.lost_sound()
            self.score.update(0)

        else:
            # reset flags and do nothing when the ball is outside measurement and bounce zone
            self.ball_action = NOTHING
            self.measure_flag = NO

    def check_score(self, player):
        return self.score.get_score(player)