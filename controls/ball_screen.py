#!/usr/bin/env python
#
# Copyright 2019 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pygame
import numpy as np
from utils.colors import *
from utils.navigation import *
from utils.resources import *
from model.circuit_grid_model import CircuitGridNode
from model import circuit_node_types as node_types


LINE_WIDTH = 1

class BallScreen(pygame.sprite.RenderPlain):
    """Make a screen for the ball"""
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.ball_screen_background = BallScreenBackground()

        pygame.sprite.RenderPlain.__init__(self, self.ball_screen_background)
        self.update()

    def update(self, *args):
        print("in CircuitGrid#update()")

        sprite_list = self.sprites()
        for sprite in sprite_list:
            sprite.update()

        self.ball_screen_background.rect.left = self.xpos
        self.ball_screen_background.rect.top = self.ypos


class BallScreenBackground(pygame.sprite.Sprite):
    """Background for circuit grid"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([1000, 500])
        self.image.convert()
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, WHITE, self.rect, LINE_WIDTH)







