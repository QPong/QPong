#
# Copyright 2022 the original author or authors.
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
Test input
"""

import unittest

import numpy as np
import pygame

from qpong.utils.level import Level
from qpong.utils.scene import Scene
from qpong.utils.ball import Ball
from qpong.utils.input import Input

from qpong.model import circuit_node_types as node_types

from qpong.utils.parameters import WINDOW_SIZE


class TestLevel(unittest.TestCase):
    """
    Unit tests for input
    """

    def setUp(self):
        """
        Set up
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode(WINDOW_SIZE, flags)

        self.scene = Scene()
        self.level = Level()
        self.input = Input()
        self.ball = Ball()

        self.level.setup(self.scene, self.ball)

    def inject_event(self, event=pygame.KEYDOWN, key=pygame.K_ESCAPE):
        """
        Inject keyboard press event to event queue
        """

        pygame.event.get()
        post_event = pygame.event.Event(event, key=key)
        pygame.event.post(post_event)

        self.input.handle_input(self.level, self.screen, self.scene)

    def test_input_initialization(self):
        """
        Test input initialization
        """

        self.assertEqual(self.input.running, True)
        self.assertEqual(self.input.gamepad_repeat_delay, 200)
        self.assertEqual(self.input.gamepad_neutral, True)
        self.assertEqual(self.input.gamepad_pressed_timer, 0)

    def test_handle_escape_keyboard_press(self):
        """
        Test handling key event for quiting pygame
        """

        self.inject_event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        self.assertEqual(self.input.running, False)

    def test_handle_navigation_keyboard_presses(self):
        """
        Test handling key events for navigating
        circuit grid
        """

        self.inject_event(pygame.KEYDOWN, key=pygame.K_d)

        # should have moved highlighted node right
        self.assertEqual(self.level.circuit_grid.selected_column, 1)
        self.assertEqual(self.level.circuit_grid.selected_wire, 0)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)

        # should have moved highlighted node left
        self.assertEqual(self.level.circuit_grid.selected_column, 0)
        self.assertEqual(self.level.circuit_grid.selected_wire, 0)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_s)

        # should have moved highlighted node down
        self.assertEqual(self.level.circuit_grid.selected_column, 0)
        self.assertEqual(self.level.circuit_grid.selected_wire, 1)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_w)

        # should have moved highlighted node u
        self.assertEqual(self.level.circuit_grid.selected_column, 0)
        self.assertEqual(self.level.circuit_grid.selected_wire, 0)

    def test_handle_single_qubit_gate_keyboard_presses(self):
        """
        Test handling key events for placing single
        qubit gates on circuit grid
        """

        # 0 X-Y-Z-H--
        # 1 ---------
        # 2 ---------

        self.inject_event(pygame.KEYDOWN, key=pygame.K_x)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_d)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_y)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_d)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_z)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_d)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_h)

        self.assertEqual(
            node_types.X, self.level.circuit_grid_model.get_node_gate_part(0, 0)
        )
        self.assertEqual(
            node_types.Y, self.level.circuit_grid_model.get_node_gate_part(0, 1)
        )
        self.assertEqual(
            node_types.Z, self.level.circuit_grid_model.get_node_gate_part(0, 2)
        )
        self.assertEqual(
            node_types.H, self.level.circuit_grid_model.get_node_gate_part(0, 3)
        )

        # 0 ---------
        # 1 ---------
        # 2 ---------

        self.inject_event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_SPACE)

        self.assertEqual(
            node_types.EMPTY, self.level.circuit_grid_model.get_node_gate_part(0, 0)
        )
        self.assertEqual(
            node_types.EMPTY, self.level.circuit_grid_model.get_node_gate_part(0, 1)
        )
        self.assertEqual(
            node_types.EMPTY, self.level.circuit_grid_model.get_node_gate_part(0, 2)
        )
        self.assertEqual(
            node_types.EMPTY, self.level.circuit_grid_model.get_node_gate_part(0, 3)
        )

        # 0 Rx--------
        # 1 Ry--------
        # 2 Rz--------

        self.inject_event(pygame.KEYDOWN, key=pygame.K_x)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_s)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_y)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_s)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_z)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_LEFT)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_LEFT)

        node1 = self.level.circuit_grid_model.get_node(0, 0)
        node2 = self.level.circuit_grid_model.get_node(1, 0)
        node3 = self.level.circuit_grid_model.get_node(2, 0)

        self.assertEqual(node_types.X, node1.node_type)
        self.assertEqual(np.pi / 8, node1.radians)

        self.assertEqual(node_types.Y, node2.node_type)
        self.assertEqual(np.pi / 4, node2.radians)

        self.assertEqual(node_types.Z, node3.node_type)
        self.assertAlmostEqual(2 * np.pi - np.pi / 4, node3.radians)

    def test_handle_multi_qubit_gate_keyboard_presses(self):
        # pylint: disable=too-many-statements
        """
        Test handling key events placing for multi
        qubit gates on circuit grid
        """
        # 0 X-Y-Z-H--
        # 1 |-|-|-|--
        # 2 ---------

        # cx
        self.inject_event(pygame.KEYDOWN, key=pygame.K_x)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_c)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_d)

        # cy
        self.inject_event(pygame.KEYDOWN, key=pygame.K_y)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_c)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_d)
        # cz
        self.inject_event(pygame.KEYDOWN, key=pygame.K_z)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_c)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_d)

        # ch
        self.inject_event(pygame.KEYDOWN, key=pygame.K_h)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_c)

        node1 = self.level.circuit_grid_model.get_node(0, 0)
        node2 = self.level.circuit_grid_model.get_node(0, 1)
        node3 = self.level.circuit_grid_model.get_node(0, 2)
        node4 = self.level.circuit_grid_model.get_node(0, 3)

        self.assertEqual(node_types.X, node1.node_type)
        self.assertEqual(1, node1.ctrl_a)
        self.assertEqual(-1, node1.ctrl_b)

        self.assertEqual(node_types.Y, node2.node_type)
        self.assertEqual(1, node2.ctrl_a)
        self.assertEqual(-1, node2.ctrl_b)

        self.assertEqual(node_types.Z, node3.node_type)
        self.assertEqual(1, node3.ctrl_a)
        self.assertEqual(-1, node3.ctrl_b)

        self.assertEqual(node_types.H, node4.node_type)
        self.assertEqual(1, node4.ctrl_a)
        self.assertEqual(-1, node4.ctrl_b)

        # 0 X-Y-Z-H--
        # 1 |-|-|-|--
        # 2 |-|-|-|--

        self.inject_event(pygame.KEYDOWN, key=pygame.K_DOWN)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_DOWN)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_DOWN)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)
        self.inject_event(pygame.KEYDOWN, key=pygame.K_DOWN)

        node1 = self.level.circuit_grid_model.get_node(0, 0)
        node2 = self.level.circuit_grid_model.get_node(0, 1)
        node3 = self.level.circuit_grid_model.get_node(0, 2)
        node4 = self.level.circuit_grid_model.get_node(0, 3)

        self.assertEqual(node_types.X, node1.node_type)
        self.assertEqual(2, node1.ctrl_a)
        self.assertEqual(-1, node1.ctrl_b)

        self.assertEqual(node_types.Y, node2.node_type)
        self.assertEqual(2, node2.ctrl_a)
        self.assertEqual(-1, node2.ctrl_b)

        self.assertEqual(node_types.Z, node3.node_type)
        self.assertEqual(2, node3.ctrl_a)
        self.assertEqual(-1, node3.ctrl_b)

        self.assertEqual(node_types.H, node4.node_type)
        self.assertEqual(2, node4.ctrl_a)
        self.assertEqual(-1, node4.ctrl_b)

    def tearDown(self):
        """
        Tear down
        """

        pygame.quit()
