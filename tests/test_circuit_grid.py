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

    def setUp(self):
        """
        Set up
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        qubit_num = 4
        self.circuit_grid_model = CircuitGridModel(qubit_num, CIRCUIT_DEPTH)
        self.grid = CircuitGrid(0, 0.7 * WINDOW_HEIGHT, self.circuit_grid_model)

    def test_circuit_grid_initialization(self):
        """
        Test circuit grid initialization
        """

        self.assertEqual(self.grid.selected_wire, 0)
        self.assertEqual(self.grid.selected_column, 0)
        self.assertEqual(self.grid.xpos, 0)
        self.assertEqual(self.grid.ypos, 0.7 * WINDOW_HEIGHT)

    def test_highlight_selected_node(self):
        """
        Test highlight selected node
        """

        self.grid.highlight_selected_node(1, 1)

        self.assertEqual(self.grid.selected_wire, 1)
        self.assertEqual(self.grid.selected_column, 1)

        self.grid.highlight_selected_node(2, 2)

        self.assertEqual(self.grid.selected_wire, 2)
        self.assertEqual(self.grid.selected_column, 2)

    def test_reset_cursor(self):
        """
        Test reset cursor
        """

        self.grid.highlight_selected_node(2, 2)
        self.grid.reset_cursor()

        self.assertEqual(self.grid.selected_column, 0)
        self.assertEqual(self.grid.selected_wire, 0)

    def test_move_to_adjacent_node(self):
        """
        Test move cursor to adjacent node
        """

        self.grid.move_to_adjacent_node(MOVE_RIGHT)

        self.assertEqual(self.grid.selected_column, 1)
        self.assertEqual(self.grid.selected_wire, 0)

        self.grid.move_to_adjacent_node(MOVE_DOWN)

        self.assertEqual(self.grid.selected_column, 1)
        self.assertEqual(self.grid.selected_wire, 1)

        self.grid.move_to_adjacent_node(MOVE_LEFT)

        self.assertEqual(self.grid.selected_column, 0)
        self.assertEqual(self.grid.selected_wire, 1)

        self.grid.move_to_adjacent_node(MOVE_UP)

        self.assertEqual(self.grid.selected_column, 0)
        self.assertEqual(self.grid.selected_wire, 0)

    def test_get_selected_node_gate_part(self):
        """
        Test getting gate on currently selected node
        """

        node1 = CircuitGridNode(node_types.X)
        node2 = CircuitGridNode(node_types.Y)
        node3 = CircuitGridNode(node_types.Z)

        self.circuit_grid_model.set_node(0, 1, node1)
        self.circuit_grid_model.set_node(1, 0, node2)
        self.circuit_grid_model.set_node(2, 0, node3)

        self.grid.move_to_adjacent_node(MOVE_RIGHT)

        selected_gate = self.grid.get_selected_node_gate_part()
        self.assertEqual(node1.node_type, selected_gate)

        self.grid.move_to_adjacent_node(MOVE_LEFT)
        self.grid.move_to_adjacent_node(MOVE_DOWN)

        selected_gate = self.grid.get_selected_node_gate_part()
        self.assertEqual(node2.node_type, selected_gate)

        self.grid.move_to_adjacent_node(MOVE_DOWN)

        selected_gate = self.grid.get_selected_node_gate_part()
        self.assertEqual(node3.node_type, selected_gate)

    def test_handle_single_qubit_gate_inputs(self):
        """
        Test handling input placing single
        qubit gates on circuit grid
        """

        # 0 X--------
        # 1 Y--------
        # 2 Z--------
        # 3 H--------

        self.grid.handle_input_x()
        self.grid.move_to_adjacent_node(MOVE_DOWN)
        self.grid.handle_input_y()
        self.grid.move_to_adjacent_node(MOVE_DOWN)
        self.grid.handle_input_z()
        self.grid.move_to_adjacent_node(MOVE_DOWN)
        self.grid.handle_input_h()

        self.assertEqual(node_types.X, self.circuit_grid_model.get_node_gate_part(0, 0))
        self.assertEqual(node_types.Y, self.circuit_grid_model.get_node_gate_part(1, 0))
        self.assertEqual(node_types.Z, self.circuit_grid_model.get_node_gate_part(2, 0))
        self.assertEqual(node_types.H, self.circuit_grid_model.get_node_gate_part(3, 0))

        # 0 ---------
        # 1 ---------
        # 2 ---------
        # 3 ---------

        self.grid.handle_input_delete()
        self.grid.move_to_adjacent_node(MOVE_UP)
        self.grid.handle_input_delete()
        self.grid.move_to_adjacent_node(MOVE_UP)
        self.grid.handle_input_delete()
        self.grid.move_to_adjacent_node(MOVE_UP)
        self.grid.handle_input_delete()

        self.assertEqual(
            node_types.EMPTY, self.circuit_grid_model.get_node_gate_part(1, 0)
        )
        self.assertEqual(
            node_types.EMPTY, self.circuit_grid_model.get_node_gate_part(1, 0)
        )
        self.assertEqual(
            node_types.EMPTY, self.circuit_grid_model.get_node_gate_part(2, 0)
        )
        self.assertEqual(
            node_types.EMPTY, self.circuit_grid_model.get_node_gate_part(3, 0)
        )

    def test_handle_multi_gate_inputs(self):
        """
        Test handling input placing multi
        qubit gates on circuit grid
        """

        # 0 |-----|--
        # 1 X-----H--
        # 2 --Y-Z----
        # 3 --|-|----

        self.grid.move_to_adjacent_node(MOVE_DOWN)

        self.grid.handle_input_x()
        self.grid.handle_input_ctrl()

        self.grid.move_to_adjacent_node(MOVE_RIGHT)
        self.grid.move_to_adjacent_node(MOVE_DOWN)

        self.grid.handle_input_y()
        self.grid.handle_input_ctrl()
        self.grid.handle_input_move_ctrl(MOVE_DOWN)

        self.grid.move_to_adjacent_node(MOVE_RIGHT)

        self.grid.handle_input_z()
        self.grid.handle_input_ctrl()
        self.grid.handle_input_move_ctrl(MOVE_DOWN)

        self.grid.move_to_adjacent_node(MOVE_RIGHT)
        self.grid.move_to_adjacent_node(MOVE_UP)

        self.grid.handle_input_h()
        self.grid.handle_input_ctrl()

        node1 = self.circuit_grid_model.get_node(1, 0)
        node2 = self.circuit_grid_model.get_node(2, 1)
        node3 = self.circuit_grid_model.get_node(2, 2)
        node4 = self.circuit_grid_model.get_node(1, 3)

        self.assertEqual(node_types.X, node1.node_type)
        self.assertEqual(0, node1.ctrl_a)
        self.assertEqual(-1, node1.ctrl_b)

        self.assertEqual(node_types.Y, node2.node_type)
        self.assertEqual(3, node2.ctrl_a)
        self.assertEqual(-1, node2.ctrl_b)

        self.assertEqual(node_types.Z, node3.node_type)
        self.assertEqual(3, node3.ctrl_a)
        self.assertEqual(-1, node3.ctrl_b)

        self.assertEqual(node_types.H, node4.node_type)
        self.assertEqual(0, node4.ctrl_a)
        self.assertEqual(-1, node4.ctrl_b)

    def tearDown(self):
        """
        Tear down
        """

        pygame.quit()
