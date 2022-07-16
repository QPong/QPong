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
Test states utilities
"""

import unittest

import pygame

from qpong.utils.resources import load_font, load_sound, load_image

from qpong.utils.parameters import WINDOW_SIZE


class TestResources(unittest.TestCase):
    """
    Unit tests for resource loading utilities
    """

    def setUp(self):
        """
        Set up
        """

        pygame.init()

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        _ = pygame.display.set_mode(WINDOW_SIZE, flags)

        self.bit_font = load_font("bit5x3.ttf")

        self.sound1 = load_sound("4384__noisecollector__pongblipd4.wav")
        self.sound2 = load_sound("4390__noisecollector__pongblipf-4.wav")
        self.sound3 = load_sound("4391__noisecollector__pongblipf-5.wav")

        self.image1 = load_image("gate_images/h_gate.png")
        self.image2 = load_image("gate_images/not_gate.png")

    def test_load_font(self):
        """
        Test load font
        """

        self.assertEqual(self.bit_font is not None, True)

    def test_load_sound(self):
        """
        Test load sound
        """

        self.assertEqual(self.sound1 is not None, True)
        self.assertEqual(self.sound2 is not None, True)
        self.assertEqual(self.sound3 is not None, True)

    def test_load_image(self):
        """
        Test load image
        """

        self.assertEqual(self.image1 is not None, True)
        self.assertEqual(self.image2 is not None, True)

    def tearDown(self):
        """
        Tear down
        """

        pygame.quit()
