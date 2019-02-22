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
from utils.navigation import *
from model import circuit_node_types as node_types

GRID_WIDTH = 66
GRID_HEIGHT = 66
LINE_WIDTH = 1


class CircuitGrid(pygame.sprite.RenderPlain):
    """Enables interaction with circuit"""
    def __init__(self, xpos, ypos, circuit_grid_model):
        self.xpos = xpos
        self.ypos = ypos
        self.circuit_grid_model = circuit_grid_model
        self.selected_wire = 0
        self.selected_column = 0
        self.circuit_grid_background = CircuitGridBackground(circuit_grid_model)
        self.circuit_grid_cursor = CircuitGridCursor()
        pygame.sprite.RenderPlain.__init__(self, self.circuit_grid_background,
                                           self.circuit_grid_cursor)

        self.circuit_grid_background.rect.left = self.xpos
        self.circuit_grid_background.rect.top = self.ypos

        self.highlight_selected_node(self.selected_wire, self.selected_column)

    def highlight_selected_node(self, wire_num, column_num):
        self.selected_wire = wire_num
        self.selected_column = column_num
        self.circuit_grid_cursor.rect.left = self.xpos + GRID_WIDTH * (self.selected_column + 1)
        self.circuit_grid_cursor.rect.top = self.ypos + GRID_HEIGHT * (self.selected_wire + 0.5)

    def move_to_adjacent_node(self, direction):
        if direction == MOVE_LEFT and self.selected_column > 0:
            self.selected_column -= 1
        elif direction == MOVE_RIGHT and self.selected_column < self.circuit_grid_model.max_columns - 1:
            self.selected_column += 1
        elif direction == MOVE_UP and self.selected_wire > 0:
            self.selected_wire -= 1
        elif direction == MOVE_DOWN and self.selected_wire < self.circuit_grid_model.max_wires - 1:
            self.selected_wire += 1

        self.highlight_selected_node(self.selected_wire, self.selected_column)

    def get_selected_node_gate_part(self):
        return self.circuit_grid_model.get_node_gate_part(self.selected_wire, self.selected_column)

    def handle_input_x(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        print('In handle_input_x, node_type in selected node is: ', selected_node_gate_part)
        if selected_node_gate_part == node_types.EMPTY or \
                selected_node_gate_part == node_types.IDEN:
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, node_types.X)

    def handle_input_delete(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        print('In handle_input_delete, node_type in selected node is: ', selected_node_gate_part)
        if selected_node_gate_part == node_types.X or \
            selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z or \
                selected_node_gate_part == node_types.H:
            control_wire_num = self.circuit_grid_model.get_node(self.selected_wire, self.selected_column).ctrl_a
            if control_wire_num != -1:
                # TODO: If this is a controlled gate, remove the connecting TRACE parts between the gate and the control
                #       and replace with placeholders (IDEN for now?)
                # ALSO: Refactor with similar code in this method
                for wire_idx in range(min(self.selected_wire, control_wire_num),
                                      max(self.selected_wire, control_wire_num) + 1):
                    print("Replacing wire ", wire_idx, " in column ",  self.selected_column)
                    self.circuit_grid_model.set_node(wire_idx, self.selected_column, node_types.IDEN)

        if selected_node_gate_part == node_types.CTRL:
            gate_wire_num = \
                self.circuit_grid_model.get_gate_wire_for_control_node(self.selected_wire,
                                                                       self.selected_column)
            for wire_idx in range(min(self.selected_wire, gate_wire_num),
                                  max(self.selected_wire, gate_wire_num) + 1):
                print("Replacing wire ", wire_idx, " in column ", self.selected_column)
                self.circuit_grid_model.set_node(wire_idx, self.selected_column, node_types.IDEN)
        elif selected_node_gate_part != node_types.IDEN and \
                selected_node_gate_part != node_types.SWAP and \
                selected_node_gate_part != node_types.CTRL and \
                selected_node_gate_part != node_types.TRACE:
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, node_types.IDEN)


class CircuitGridBackground(pygame.sprite.Sprite):
    """Background for circuit grid"""
    def __init__(self, circuit_grid_model):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([GRID_WIDTH * (circuit_grid_model.max_columns + 2),
                                     GRID_HEIGHT * (circuit_grid_model.max_wires + 1)])
        self.image.convert()
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
        self.image.convert()
        self.image.fill(WHITE)
        # self.image.set_alpha(0)

        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, GREEN, self.rect, LINE_WIDTH * 4)


