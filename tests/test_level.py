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

    def setUp(self):
        """
        Set up
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        self.scene = Scene()
        self.level = Level()
        self.ball = Ball()

    def test_level_initialization(self):
        """
        Test level initialization
        """

        self.assertEqual(self.level.level, 3)
        self.assertEqual(self.level.win, False)
        self.assertEqual(self.level.circuit is None, True)
        self.assertEqual(self.level.circuit_grid is None, True)
        self.assertEqual(self.level.circuit_grid_model is None, True)
        self.assertEqual(self.level.statevector_grid is None, True)
        self.assertEqual(self.level.right_statevector is None, True)

    def test_level_setup(self):
        """
        Test level setup
        """

        self.level.setup(self.scene, self.ball)

        self.assertEqual(self.scene.qubit_num, 3)
        self.assertEqual(self.level.circuit is None, False)
        self.assertEqual(self.level.circuit_grid is None, False)
        self.assertEqual(self.level.circuit_grid_model is None, False)
        self.assertEqual(self.level.statevector_grid is None, False)
        self.assertEqual(self.level.right_statevector is None, False)

    def tearDown(self):
        """
        Tear down
        """

        pygame.quit()
