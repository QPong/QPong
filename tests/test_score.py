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
Test score
"""

import unittest

from qpong.utils.score import Score


class TestScene(unittest.TestCase):
    """
    Unit tests for score
    """

    def setUp(self):
        """
        Set up
        """

        self.score = Score()

    def test_score_initialization(self):
        """
        Test score initialization
        """

        self.assertEqual(self.score.player, 0)
        self.assertEqual(self.score.computer, 0)

    def test_score_update(self):
        """
        Test score update
        """

        self.score.update(0)

        self.assertEqual(self.score.computer, 1)
        self.assertEqual(self.score.player, 0)

        self.score.update(1)

        self.assertEqual(self.score.computer, 1)
        self.assertEqual(self.score.player, 1)

    def test_score_reset(self):
        """
        Test score reset
        """

        self.score.update(0)
        self.score.update(1)

        self.score.reset_score()

        self.assertEqual(self.score.computer, 0)
        self.assertEqual(self.score.player, 0)

    def test_score_getter(self):
        """
        Test score getter
        """

        self.score.update(0)
        self.score.update(1)

        self.assertEqual(self.score.get_score(0), 1)
        self.assertEqual(self.score.get_score(1), 1)
