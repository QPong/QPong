#!/usr/bin/env python
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

from utils.parameters import *
from utils.fonts import ARIAL_30, ARIAL_80
from utils.colors import *

class Scene():
    """Displayer Game Over screen and handle play again"""

    def gameover(self,screen,score,win_score):
        if score.get_score(CLASSICAL_COMPUTER) >= win_score:
            gameovertext = "Game Over"
            text = ARIAL_80.render(gameovertext, 1, WHITE)
            textpos= (450,250)
            screen.blit(text, textpos)

        if score.get_score(QUANTUM_COMPUTER) >= win_score:
            gameovertext = "Congratulations!"
            text = ARIAL_80.render(gameovertext, 5, WHITE)
            textpos= (370,250)
            screen.blit(text, textpos)
