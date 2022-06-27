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
A container for managing game screens
"""

import pygame

from qpong.utils.parameters import (
    WIDTH_UNIT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    QUANTUM_COMPUTER,
    CLASSICAL_COMPUTER,
    EASY,
    NORMAL,
    EXPERT,
)
from qpong.utils.colors import WHITE, BLACK, GRAY
from qpong.utils import gamepad
from qpong.utils.font import Font


class Scene:
    """
    Display Game Over screen and handle play again
    """

    def __init__(self):
        super().__init__()

        self.begin = False
        self.restart = False
        self.qubit_num = 3
        self.font = Font()

    def start(self, screen, ball):
        # pylint: disable=too-many-branches disable=too-many-return-statements
        """
        Show start screen
        """

        screen.fill(BLACK)

        gameover_text = "QPong"
        text = self.font.gameover_font.render(gameover_text, 1, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 15))
        screen.blit(text, text_pos)

        gameover_text = "Select difficulty level"
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 30))
        screen.blit(text, text_pos)

        gameover_text = "[A] Easy  "
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 35))
        screen.blit(text, text_pos)

        gameover_text = "[B] Normal"
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
        screen.blit(text, text_pos)

        gameover_text = "[X] Expert"
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 45))
        screen.blit(text, text_pos)

        self.credits(screen)

        while not self.begin:

            for event in pygame.event.get():
                pygame.event.pump()

                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == gamepad.BTN_A:
                        # easy mode
                        ball.initial_speed_factor = EASY
                        return True
                    if event.button == gamepad.BTN_B:
                        # normal mode
                        ball.initial_speed_factor = NORMAL
                        return True
                    if event.button == gamepad.BTN_X:
                        # expert mode
                        ball.initial_speed_factor = EXPERT
                        return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_a:
                        # easy mode
                        ball.initial_speed_factor = EASY
                        return True
                    if event.key == pygame.K_b:
                        # normal mode
                        ball.initial_speed_factor = NORMAL
                        return True
                    if event.key == pygame.K_x:
                        # expert mode
                        ball.initial_speed_factor = EXPERT
                        return True

            if self.begin:
                # reset all parameters to restart the game
                screen.fill(BLACK)

            pygame.display.flip()

        # reset restart flag when self.restart = True and the while ends
        self.begin = False

    def gameover(self, screen, player):
        """
        Display Game Over screen
        """
        if player == CLASSICAL_COMPUTER:

            screen.fill(BLACK)

            gameover_text = "Game Over"
            text = self.font.gameover_font.render(gameover_text, 1, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
            screen.blit(text, text_pos)

            gameover_text = "Classical computer"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
            screen.blit(text, text_pos)

            gameover_text = "still rules the world"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
            screen.blit(text, text_pos)

            self.credits(screen)

        if player == QUANTUM_COMPUTER:

            screen.fill(BLACK)

            gameover_text = "Congratulations!"
            text = self.font.gameover_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
            screen.blit(text, text_pos)

            gameover_text = "You demonstrated quantum supremacy"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
            screen.blit(text, text_pos)

            gameover_text = "for the first time in human history!"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
            screen.blit(text, text_pos)

            self.credits(screen)

    @staticmethod
    def dashed_line(screen, ball):
        """
        Show dashed line diving the playing field
        """

        for i in range(10, ball.screenheight, 2 * WIDTH_UNIT):  # draw dashed line
            pygame.draw.rect(
                screen,
                GRAY,
                (WINDOW_WIDTH // 2 - 5, i, 0.5 * WIDTH_UNIT, WIDTH_UNIT),
                0,
            )

    def score(self, screen, ball):
        """
        Show score for both player
        """
        # Print the score
        text = self.font.player_font.render("Classical Computer", 1, GRAY)
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.25) + WIDTH_UNIT * 4.5, WIDTH_UNIT * 1.5)
        )
        screen.blit(text, text_pos)

        text = self.font.player_font.render("Quantum Computer", 1, GRAY)
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.75) - WIDTH_UNIT * 4.5, WIDTH_UNIT * 1.5)
        )
        screen.blit(text, text_pos)

        score_print = str(ball.check_score(0))
        text = self.font.score_font.render(score_print, 1, GRAY)
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.25) + WIDTH_UNIT * 4.5, WIDTH_UNIT * 8)
        )
        screen.blit(text, text_pos)

        score_print = str(ball.check_score(1))
        text = self.font.score_font.render(score_print, 1, GRAY)
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.75) - WIDTH_UNIT * 4.5, WIDTH_UNIT * 8)
        )
        screen.blit(text, text_pos)

    def credits(self, screen):
        """
        Show credits screen
        """
        credit_text = "Credits"
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 8)
        )
        screen.blit(text, text_pos)

        credit_text = (
            "Made by Huang Junye, James Weaver, Jarrod Reilly and Anastasia Jeffery"
        )
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 5)
        )
        screen.blit(text, text_pos)

        credit_text = "Initiated at IBM Qiskit Camp 2019"
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 3)
        )
        screen.blit(text, text_pos)

        credit_text = "Powered by JavaFXpert/quantum-circuit-game"
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 1)
        )
        screen.blit(text, text_pos)

    def replay(self, screen, score, circuit_grid_model, circuit_grid):
        """
        Pause the game and ask if the player wants to play again
        """
        blink_time = pygame.time.get_ticks()

        while not self.restart:

            for event in pygame.event.get():
                pygame.event.pump()

                if event.type == pygame.QUIT:
                    pygame.quit()
                else:
                    self.restart = True

            if self.restart:
                # reset all parameters to restart the game
                score.reset_score()
                circuit_grid_model.reset_circuit()
                circuit_grid.update()
                circuit_grid.reset_cursor()

            # Make blinking text
            if pygame.time.get_ticks() - blink_time > 1000:
                blink_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - blink_time > 500:
                replay_text = "Press Any Key to Play Again"
                text = self.font.replay_font.render(replay_text, 1, WHITE)
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
                screen.blit(text, text_pos)
                pygame.display.flip()
            else:
                # show a black box to blink the text every 0.5s
                pygame.draw.rect(
                    screen,
                    BLACK,
                    (
                        WIDTH_UNIT * 10,
                        WIDTH_UNIT * 35,
                        WIDTH_UNIT * 80,
                        WIDTH_UNIT * 10,
                    ),
                )
                pygame.display.flip()

        # reset restart flag when self.restart = True and the while ends
        self.restart = False
