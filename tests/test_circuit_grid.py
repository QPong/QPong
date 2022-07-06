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

from qpong.model.circuit_grid_model import CircuitGridModel, CircuitGridNode
from qpong.model import circuit_node_types as node_types

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

    def test_get_selected_node_gate_part(self):
        """
        Test getting gate on currently selected node
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        node1 = CircuitGridNode(node_types.Y)
        node2 = CircuitGridNode(node_types.X)
        node3 = CircuitGridNode(node_types.Z)

        circuit_grid_model.set_node(0, 1, node1)
        circuit_grid_model.set_node(1, 0, node2)
        circuit_grid_model.set_node(2, 0, node3)

        grid.move_to_adjacent_node(MOVE_RIGHT)

        selected_gate = grid.get_selected_node_gate_part()
        self.assertEqual(node1.node_type, selected_gate)

        grid.move_to_adjacent_node(MOVE_LEFT)
        grid.move_to_adjacent_node(MOVE_DOWN)

        selected_gate = grid.get_selected_node_gate_part()
        self.assertEqual(node2.node_type, selected_gate)

        grid.move_to_adjacent_node(MOVE_DOWN)

        selected_gate = grid.get_selected_node_gate_part()
        self.assertEqual(node3.node_type, selected_gate)

        pygame.quit()

    def test_handle_input_x(self):
        """
        Test handling input to place X gate on currently selected node
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        self.assertEqual(
            node_types.EMPTY, grid.circuit_grid_model.get_node_gate_part(0, 0)
        )

        grid.handle_input_x()

        self.assertEqual(node_types.X, grid.circuit_grid_model.get_node_gate_part(0, 0))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_x()

        self.assertEqual(node_types.X, grid.circuit_grid_model.get_node_gate_part(0, 1))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_x()

        self.assertEqual(node_types.X, grid.circuit_grid_model.get_node_gate_part(0, 2))

        grid.move_to_adjacent_node(MOVE_DOWN)

        grid.handle_input_x()

        self.assertEqual(node_types.X, grid.circuit_grid_model.get_node_gate_part(1, 2))

        pygame.quit()

    def test_handle_input_y(self):
        """
        Test handling input to place Y gate on currently selected node
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        self.assertEqual(
            node_types.EMPTY, grid.circuit_grid_model.get_node_gate_part(0, 0)
        )

        grid.handle_input_y()

        self.assertEqual(node_types.Y, grid.circuit_grid_model.get_node_gate_part(0, 0))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_y()

        self.assertEqual(node_types.Y, grid.circuit_grid_model.get_node_gate_part(0, 1))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_y()

        self.assertEqual(node_types.Y, grid.circuit_grid_model.get_node_gate_part(0, 2))

        grid.move_to_adjacent_node(MOVE_DOWN)

        grid.handle_input_y()

        self.assertEqual(node_types.Y, grid.circuit_grid_model.get_node_gate_part(1, 2))

        pygame.quit()

    def test_handle_input_z(self):
        """
        Test handling input to place Z gate on currently selected node
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        self.assertEqual(
            node_types.EMPTY, grid.circuit_grid_model.get_node_gate_part(0, 0)
        )

        grid.handle_input_z()

        self.assertEqual(node_types.Z, grid.circuit_grid_model.get_node_gate_part(0, 0))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_z()

        self.assertEqual(node_types.Z, grid.circuit_grid_model.get_node_gate_part(0, 1))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_z()

        self.assertEqual(node_types.Z, grid.circuit_grid_model.get_node_gate_part(0, 2))

        grid.move_to_adjacent_node(MOVE_DOWN)

        grid.handle_input_z()

        self.assertEqual(node_types.Z, grid.circuit_grid_model.get_node_gate_part(1, 2))

        pygame.quit()

    def test_handle_input_h(self):
        """
        Test handling input to place H gate on currently selected node
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 3
        circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, circuit_grid_model)

        self.assertEqual(
            node_types.EMPTY, grid.circuit_grid_model.get_node_gate_part(0, 0)
        )

        grid.handle_input_h()

        self.assertEqual(node_types.H, grid.circuit_grid_model.get_node_gate_part(0, 0))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_h()

        self.assertEqual(node_types.H, grid.circuit_grid_model.get_node_gate_part(0, 1))

        grid.move_to_adjacent_node(MOVE_RIGHT)

        grid.handle_input_h()

        self.assertEqual(node_types.H, grid.circuit_grid_model.get_node_gate_part(0, 2))

        grid.move_to_adjacent_node(MOVE_DOWN)

        grid.handle_input_h()

        self.assertEqual(node_types.H, grid.circuit_grid_model.get_node_gate_part(1, 2))

        pygame.quit()
