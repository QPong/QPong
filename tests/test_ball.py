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
Test ball
"""

import unittest

from qpong.utils.ball import Ball

from qpong.utils.parameters import (
    LEFT,
    RIGHT,
    NOTHING,
    NO,
    WINDOW_HEIGHT,
)


class TestBall(unittest.TestCase):
    """
    Unit tests for QPong ball
    """

    def setUp(self):
        """
        Set up
        """

        self.ball = Ball()

    def test_ball_initialization(self):
        """
        Test ball initialization
        """

        self.assertEqual(
            self.ball.xpos, self.ball.left_edge + self.ball.width_unit * 15
        )
        self.assertEqual(self.ball.ypos, 0.7 * WINDOW_HEIGHT / 2)
        self.assertEqual(self.ball.initial_speed_factor, 0.8)
        self.assertEqual(self.ball.ball_action, NOTHING)
        self.assertEqual(self.ball.measure_flag, NO)
        self.assertEqual(self.ball.reset_position, RIGHT)

    def test_reset_ball(self):
        """
        Test ball reset
        """

        self.ball.reset()

        self.assertEqual(
            self.ball.xpos, self.ball.right_edge - self.ball.width_unit * 15
        )
        self.assertEqual(self.ball.ypos, 0.7 * WINDOW_HEIGHT / 2)
        self.assertEqual(self.ball.reset_position, LEFT)
