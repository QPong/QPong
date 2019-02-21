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
from utils.colors import *

GRID_WIDTH = 66
GRID_HEIGHT = 66
LINE_WIDTH = 1


class CircuitGrid(pygame.sprite.RenderPlain):
    """Enables interaction with circuit"""
    def __init__(self, xpos, ypos, circuit_grid_model):
        self.xpos = xpos
        self.ypos = ypos
        self.cur_wire = 0
        self.cur_column = 0
        self.circuit_grid_background = CircuitGridBackground(circuit_grid_model)
        self.circuit_grid_cursor = CircuitGridCursor()
        pygame.sprite.RenderPlain.__init__(self, self.circuit_grid_background,
                                           self.circuit_grid_cursor)

        self.circuit_grid_background.rect.left = self.xpos
        self.circuit_grid_background.rect.top = self.ypos

        self.set_cur_node(self.cur_wire, self.cur_column)

    def set_cur_node(self, wire_num, column_num):
        self.cur_wire = wire_num
        self.cur_column = column_num
        self.circuit_grid_cursor.rect.left = self.xpos + GRID_WIDTH * (self.cur_column + 1)
        self.circuit_grid_cursor.rect.top = self.ypos + GRID_HEIGHT * (self.cur_wire + 0.5)


class CircuitGridBackground(pygame.sprite.Sprite):
    """Background for circuit grid"""
    def __init__(self, circuit_grid_model):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([GRID_WIDTH * (circuit_grid_model.max_columns + 2),
                                     GRID_HEIGHT * (circuit_grid_model.max_wires + 1)])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, BLACK, self.rect, LINE_WIDTH)

        for wire_num in range(circuit_grid_model.max_wires):
            pygame.draw.line(self.image, BLACK,
                             (GRID_WIDTH * 0.5, (wire_num + 1) * GRID_HEIGHT),
                             (self.rect.width - (GRID_WIDTH * 0.5), (wire_num + 1) * GRID_HEIGHT),
                             LINE_WIDTH)


class CircuitGridCursor(pygame.sprite.Sprite):
    """Cursor to highlight current grid node"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([GRID_WIDTH, GRID_HEIGHT])
        self.image.fill(WHITE)
        # self.image.set_alpha(0)

        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, GREEN, self.rect, LINE_WIDTH * 4)


