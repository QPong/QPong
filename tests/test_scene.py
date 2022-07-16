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
Test scene
"""

import unittest

import pygame

from qpong.utils.scene import Scene
from qpong.utils.level import Level
from qpong.utils.ball import Ball

from qpong.utils.parameters import (
    WINDOW_SIZE,
    EASY,
    NORMAL,
    EXPERT,
)


class TestScene(unittest.TestCase):
    """
    Unit tests for scene
    """

    def setUp(self):
        """
        Set up.
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode(WINDOW_SIZE, flags)

        self.ball = Ball()
        self.level = Level()
        self.scene = Scene()

    @staticmethod
    def inject_event(event=pygame.KEYDOWN, key=pygame.K_ESCAPE):
        """
        Inject keyboard press event to pygame event queue
        """

        pygame.event.get()
        post_event = pygame.event.Event(event, key=key)
        pygame.event.post(post_event)

    def test_scene_initialization(self):
        """
        Test scene initialization
        """

        self.assertEqual(self.scene.begin, False)
        self.assertEqual(self.scene.restart, False)
        self.assertEqual(self.scene.qubit_num, 3)

    def test_start_scene(self):
        """
        Test start scene
        """

        # select easy mode
        self.inject_event(pygame.KEYDOWN, key=pygame.K_a)
        self.scene.start(self.screen, self.ball)
        self.assertEqual(self.ball.initial_speed_factor, EASY)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_b)
        self.scene.start(self.screen, self.ball)
        self.assertEqual(self.ball.initial_speed_factor, NORMAL)

        self.inject_event(pygame.KEYDOWN, key=pygame.K_x)
        self.scene.start(self.screen, self.ball)
        self.assertEqual(self.ball.initial_speed_factor, EXPERT)

    def tearDown(self):
        """
        Tear down
        """

        pygame.quit()
