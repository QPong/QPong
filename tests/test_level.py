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
Test level
"""

import unittest

import pygame

from qpong.utils.level import Level
from qpong.utils.scene import Scene
from qpong.utils.ball import Ball

from qpong.utils.parameters import WINDOW_SIZE


class Testlevel(unittest.TestCase):
    """
    Unit tests for level
    """

    def test_level_initialization(self):
        """
        Test level initialization
        """

        level = Level()

        self.assertEqual(level.level, 3)
        self.assertEqual(level.win, False)
        self.assertEqual(level.circuit is None, True)
        self.assertEqual(level.circuit_grid is None, True)
        self.assertEqual(level.circuit_grid_model is None, True)
        self.assertEqual(level.statevector_grid is None, True)
        self.assertEqual(level.right_statevector is None, True)

    def test_level_setup(self):
        """
        Test level setup
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        scene = Scene()
        level = Level()
        ball = Ball()

        level.setup(scene, ball)

        self.assertEqual(scene.qubit_num, 3)
        self.assertEqual(level.circuit is None, False)
        self.assertEqual(level.circuit_grid is None, False)
        self.assertEqual(level.circuit_grid_model is None, False)
        self.assertEqual(level.statevector_grid is None, False)
        self.assertEqual(level.right_statevector is None, False)

        pygame.quit()
