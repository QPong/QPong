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
Various fonts used through out the game
"""

from qpong.utils.parameters import WIDTH_UNIT

from qpong.utils.resources import load_font

# pylint: disable=too-few-public-methods
class Font:
    """
    Load fonts
    """

    def __init__(self):
        self.gameover_font = load_font("bit5x3.ttf", 10 * WIDTH_UNIT)
        self.credit_font = load_font("bit5x3.ttf", 2 * WIDTH_UNIT)
        self.replay_font = load_font("bit5x3.ttf", 5 * WIDTH_UNIT)
        self.score_font = load_font("bit5x3.ttf", 12 * WIDTH_UNIT)
        self.vector_font = load_font("bit5x3.ttf", 3 * WIDTH_UNIT)
        self.player_font = load_font("bit5x3.ttf", 3 * WIDTH_UNIT)
