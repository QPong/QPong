import math
import random

import pygame as pg

from prepare import (
    COLORS,
    SOUND_EFFECTS,
    WIDTH_UNIT,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    BALL_ACTIONS,
)

# Ball directions
LEFT = 0
RIGHT = 1

# Measurement flags
YES = 1
NO = 0


class Ball(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # get ball screen dimensions
        self._screenheight = round(WINDOW_HEIGHT * 0.7)
        self._screenwidth = WINDOW_WIDTH
        self._width_unit = WIDTH_UNIT

        self._left_edge = self._width_unit
        self._right_edge = self._screenwidth - self._left_edge

        self._top_edge = self._width_unit * 0
        self._bottom_edge = self._screenheight - self._top_edge

        # define the ball sizes
        self._height = self._width_unit
        self._width = self._width_unit

        # create a pg Surface with ball size
        self._image = pg.Surface([self._height, self._width])

        self._image.fill(COLORS["WHITE"])

        self._rect = self._image.get_rect()

        self._x = 0
        self._y = 0
        self._speed = 0
        self._initial_speed_factor = 0.8
        self._direction = 0

        # initialize ball action type, measure and bounce flags
        self._ball_action = BALL_ACTIONS["NOTHING"]
        self._measure_flag = NO

        # initialize ball reset on the left
        self._reset_position = LEFT
        self.reset()

    @property
    def initial_speed_factor(self):
        return self._initial_speed_factor

    @initial_speed_factor.setter
    def initial_speed_factor(self, value):
        self._initial_speed_factor = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def ball_action(self):
        return self._ball_action

    @ball_action.setter
    def ball_action(self, value):
        self._ball_action = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    def update(self):
        radians = math.radians(self._direction)

        self._x += self._speed * math.sin(radians)
        self._y -= self._speed * math.cos(radians)

        # Update ball position
        self._rect.x = self._x
        self._rect.y = self._y

        if self._y <= self._top_edge:
            self._direction = (180 - self._direction) % 360
            SOUND_EFFECTS["EDGE"].play()
        if self._y > self._bottom_edge - 1.0 * self._height:
            self._direction = (180 - self._direction) % 360
            SOUND_EFFECTS["EDGE"].play()

    def reset(self):
        self._y = self._screenheight / 2
        self._speed = self._width_unit * self._initial_speed_factor

        # alternate reset at left and right
        if self._reset_position == LEFT:
            self._x = self._left_edge + self._width_unit * 15
            self._direction = random.randrange(30, 120)
            self._reset_position = RIGHT
        else:
            self._x = self._right_edge - self._width_unit * 15
            self._direction = random.randrange(-120, -30)
            self._reset_position = LEFT

    def bounce_edge(self):
        self._direction = (360 - self._direction) % 360
        self._speed *= 1.1
        SOUND_EFFECTS["BOUNCE"].play()

    # 1 = comp, 2 = player, none = 0
    def action(self, players):
        if self._x < self._left_edge:
            # reset the ball when it reaches beyond left edge
            self.reset()
            players[1].score += 1
            SOUND_EFFECTS["LOST"].play()

        elif (
            self._left_edge + 10 * self._width_unit
            <= self._x
            < self._left_edge + 12 * self._width_unit
        ):
            # measure the ball when it reaches the left measurement zone
            if self._measure_flag == NO:
                self._ball_action = BALL_ACTIONS["MEASURE_LEFT"]
                self._measure_flag = YES
            else:
                self._ball_action = BALL_ACTIONS["NOTHING"]

        elif (
            self._right_edge - 12 * self._width_unit
            <= self._x
            < self._right_edge - 10 * self._width_unit
        ):
            # measure the ball when it reaches the right measurement zone
            if self._measure_flag == NO:
                # do measurement if not yet done
                self._ball_action = BALL_ACTIONS["MEASURE_RIGHT"]
                self._measure_flag = YES
            else:
                # do nothing if measurement was done already
                self._ball_action = BALL_ACTIONS["NOTHING"]

        elif self._x > self._right_edge:
            # reset the ball when it reaches beyond right edge
            self.reset()
            players[0].score += 1
            SOUND_EFFECTS["LOST"].play()
        else:
            # reset flags and do nothing when the ball is outside measurement and bounce zone
            self._ball_action = BALL_ACTIONS["NOTHING"]
            self._measure_flag = NO
