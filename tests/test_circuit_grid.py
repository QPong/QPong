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
# pylint: disable=duplicate-code

"""
Test circuit grid
"""

import unittest

import pygame

from qpong.model.circuit_grid_model import CircuitGridModel
from qpong.controls.circuit_grid import CircuitGrid

from qpong.utils.parameters import WINDOW_SIZE, WINDOW_HEIGHT, CIRCUIT_DEPTH

from qpong.utils.navigation import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT


class TestCircuitGrid(unittest.TestCase):
    """
    Unit tests for circuit grid
    """

    def test_circuit_grid_initialization(self):
        """
        Test circuit grid initialization
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        self.assertEqual(grid.selected_wire, 0)
        self.assertEqual(grid.selected_column, 0)
        self.assertEqual(grid.xpos, 0)
        self.assertEqual(grid.ypos, 0.7 * WINDOW_HEIGHT)

        pygame.quit()

    def test_highlight_selected_node(self):
        """
        Test highlight selected node
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        grid.highlight_selected_node(1, 1)

        self.assertEqual(grid.selected_wire, 1)
        self.assertEqual(grid.selected_column, 1)

        grid.highlight_selected_node(2, 2)

        self.assertEqual(grid.selected_wire, 2)
        self.assertEqual(grid.selected_column, 2)

        pygame.quit()

    def test_reset_cursor(self):
        """
        Test reset cursor
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        grid.highlight_selected_node(2, 2)

        grid.reset_cursor()

        self.assertEqual(grid.selected_column, 0)
        self.assertEqual(grid.selected_wire, 0)

        pygame.quit()

    def test_move_to_adjacent_node(self):
        """
        Test move cursor to adjacent node
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        grid.move_to_adjacent_node(MOVE_RIGHT)

        self.assertEqual(grid.selected_column, 1)
        self.assertEqual(grid.selected_wire, 0)

        grid.move_to_adjacent_node(MOVE_DOWN)

        self.assertEqual(grid.selected_column, 1)
        self.assertEqual(grid.selected_wire, 1)

        grid.move_to_adjacent_node(MOVE_LEFT)

        self.assertEqual(grid.selected_column, 0)
        self.assertEqual(grid.selected_wire, 1)

        grid.move_to_adjacent_node(MOVE_UP)

        self.assertEqual(grid.selected_column, 0)
        self.assertEqual(grid.selected_wire, 0)

        pygame.quit()
