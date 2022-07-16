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
Test vbox
"""

import unittest

import pygame

from qpong.containers.vbox import VBox
from qpong.utils.parameters import WINDOW_SIZE


class TestVBox(unittest.TestCase):
    """
    Unit tests for VBox
    """

    def setUp(self):
        class Block(pygame.sprite.Sprite):
            # pylint: disable=too-few-public-methods
            """
            Testing block
            """

            def __init__(self, width, height):
                pygame.sprite.Sprite.__init__(self)

                self.image = pygame.Surface([width, height])

                self.rect = self.image.get_rect()

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        self.rectangle = Block(50, 10)
        self.square = Block(20, 20)
        self.vbox = VBox(50, 10, self.rectangle, self.square)

    def test_vbox_initialization(self):
        """
        Test vbox initialization
        """

        self.assertEqual(self.vbox.xpos, 50)
        self.assertEqual(self.vbox.ypos, 10)

        self.assertEqual(self.rectangle.rect.top, 10)
        self.assertEqual(self.rectangle.rect.left, 50)

        self.assertEqual(self.square.rect.top, 20)
        self.assertEqual(self.square.rect.left, 50)

    def tearDown(self):
        """
        Tear down
        """

        pygame.quit()
