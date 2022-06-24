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
Game score
"""
import pygame


class Score(pygame.sprite.Sprite):
    """
    Score container for ongoing game
    """

    def __init__(self):
        super().__init__()

        self.player = 0
        self.computer = 0

    # Player = 0, Computer = 1
    def update(self, score):
        """
        Get score for a specified player

        Parameters:
        score (integer):
        """
        if score == 0:
            self.computer += 1

        if score == 1:
            self.player += 1

    def get_score(self, player):
        """
        Get score for a specified player

        Parameters:
        player (integer):
        """
        if player == 0:
            return self.computer
        return self.player

    def reset_score(self):
        """
        Reset score
        """
        self.computer = 0
        self.player = 0
