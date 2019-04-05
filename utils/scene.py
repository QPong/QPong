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

from pygame.locals import *
from utils.parameters import *
from utils.fonts import *
from utils.colors import *
from utils.score import *
from time import sleep


class Scene():
    """Displaye Game Over screen and handle play again"""

    def __init__(self):
        super().__init__()

        self.restart = False

    def start(self,screen):
        """Displayer Start screen"""
        gameovertext = "Start?"
        text = GAMEOVER_FONT.render(gameovertext, 1, WHITE)
        textpos = (450, 250)
        screen.blit(text, textpos)

    def gameover(self,screen,score,win_score):
        """Display Game Over screen"""
        if score.get_score(CLASSICAL_COMPUTER) >= win_score:

            screen.fill(BLACK)

            gameover_text = "Game Over"
            text = GAMEOVER_FONT.render(gameover_text, 1, WHITE)
            textpos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
            screen.blit(text, textpos)

            gameover_text = "Classical computer"
            text = REPLAY_FONT.render(gameover_text, 5, WHITE)
            textpos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
            screen.blit(text, textpos)

            gameover_text = "still rules the world"
            text = REPLAY_FONT.render(gameover_text, 5, WHITE)
            textpos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
            screen.blit(text, textpos)

            self.credits(screen)
            self.replay(screen, score)

        if score.get_score(QUANTUM_COMPUTER) >= win_score:

            screen.fill(BLACK)

            gameover_text = "Congratulations!"
            text = GAMEOVER_FONT.render(gameover_text, 5, WHITE)
            textpos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
            screen.blit(text, textpos)

            gameover_text = "You demonstrated quantum supremacy"
            text = REPLAY_FONT.render(gameover_text, 5, WHITE)
            textpos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
            screen.blit(text, textpos)

            gameover_text = "for the first time in human history!"
            text = REPLAY_FONT.render(gameover_text, 5, WHITE)
            textpos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
            screen.blit(text, textpos)

            self.credits(screen)
            self.replay(screen, score)

    def credits(self,screen):
        credit_text = "Credits"
        text = CREDIT_FONT.render(credit_text, 1, WHITE)
        textpos = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - WIDTH_UNIT * 8))

        screen.blit(text, textpos)

        credit_text = "Made by Huang Junye, James Weaver, Jarrod Reilly and Anastasia Jeffery"
        text = CREDIT_FONT.render(credit_text, 1, WHITE)
        textpos = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - WIDTH_UNIT * 5))
        screen.blit(text, textpos)

        credit_text = "Initiated in IBM Qiskit Camp 2019"
        text = CREDIT_FONT.render(credit_text, 1, WHITE)
        textpos = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - WIDTH_UNIT * 3))
        screen.blit(text, textpos)

        credit_text = "Powered by JavaFXpert/quantum-circuit-game"
        text = CREDIT_FONT.render(credit_text, 1, WHITE)
        textpos = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - WIDTH_UNIT * 1))
        screen.blit(text, textpos)


    def replay(self,screen,score):
        """Pause the game and ask if the player wants to play again"""
        blink_time = pygame.time.get_ticks()

        while not self.restart:

            for event in pygame.event.get():
                pygame.event.pump()

                if event.type == QUIT:
                    pygame.quit()
                else:
                    self.restart = True

            if self.restart == True:
                # reset all parameters to restart the game
                score.reset_score()

            # Make blinking text
            if pygame.time.get_ticks()-blink_time > 1000:
                blink_time = pygame.time.get_ticks()
            if pygame.time.get_ticks()-blink_time > 500:
                replay_text = "Press Any Key to Play Again."
                text = REPLAY_FONT.render(replay_text, 1, WHITE)
                textpos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
                screen.blit(text, textpos)
                pygame.display.flip()
            else:
                # show a black box to blink the text every 0.5s
                pygame.draw.rect(screen, BLACK, (WIDTH_UNIT * 10, WIDTH_UNIT * 35, WIDTH_UNIT * 80, WIDTH_UNIT * 10))
                pygame.display.flip()



        # reset restart flag when self.restart = True and the while ends
        self.restart = False