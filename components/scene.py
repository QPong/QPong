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
import pygame as pg

from prepare import (
    COLORS,
    FONTS,
    CLASSICAL_COMPUTER,
    QUANTUM_COMPUTER_1P,
    QUANTUM_COMPUTER_2P,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    WIDTH_UNIT,
    MODES,
    GAMEPAD,
)

# Ball speed
BALL_SPEED = {"EASY": 0.3, "NORMAL": 0.6, "EXPERT": 1.5}


class Scene(object):
    """Display Game Over screen and handle play again"""

    def __init__(self, _qubit_num):
        super().__init__()

        self._begin = False
        self._restart = False
        self._qubit_num = _qubit_num
        self._game_mode = MODES["ONE_PLAYER"]

    @property
    def game_mode(self):
        return self._game_mode

    @game_mode.setter
    def game_mode(self, value):
        self._game_mode = value

    def mode(self, screen):
        """Show mode selection screen"""

        screen.fill(COLORS["BLACK"])

        gameover_text = "QPong"
        text = FONTS["GAMEOVER"].render(gameover_text, 1, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 15))
        screen.blit(text, text_pos)

        gameover_text = "Select game mode"
        text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 30))
        screen.blit(text, text_pos)

        gameover_text = "[A] CLASSICAL (CPU) vs. QUANTUM (HUMAN)"
        text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 35))
        screen.blit(text, text_pos)

        gameover_text = "[B] QUANTUM (HUMAN) vs. QUANTUM (HUMAN)"
        text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
        screen.blit(text, text_pos)

        self.credits(screen)

        while not self._begin:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                elif event.type == pg.JOYBUTTONDOWN:
                    if event.button == GAMEPAD["BTN_A"]:
                        # one player mode
                        self._game_mode = MODES["ONE_PLAYER"]
                        return True
                    elif event.button == GAMEPAD["BTN_B"]:
                        # two player mode
                        self._game_mode = MODES["TWO_PLAYER"]
                        return True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    elif event.key == pg.K_a:
                        # one player mode
                        self._game_mode = MODES["ONE_PLAYER"]
                        return True
                    elif event.key == pg.K_b:
                        # two player mode
                        self._game_mode = MODES["TWO_PLAYER"]
                        return True

            if self._begin:
                # reset all parameters to restart the game
                screen.fill(COLORS["BLACK"])

            pg.display.flip()

        # reset restart flag when self._restart = True and the while ends
        self._begin = False

    def difficulty(self, screen, ball):
        """Show difficulty selection screen"""

        screen.fill(COLORS["BLACK"])

        gameover_text = "QPong"
        text = FONTS["GAMEOVER"].render(gameover_text, 1, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 15))
        screen.blit(text, text_pos)

        gameover_text = "Select difficulty level"
        text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 30))
        screen.blit(text, text_pos)

        gameover_text = "[A] Easy  "
        text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 35))
        screen.blit(text, text_pos)

        gameover_text = "[B] Normal"
        text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
        screen.blit(text, text_pos)

        gameover_text = "[X] Expert"
        text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 45))
        screen.blit(text, text_pos)

        self.credits(screen)

        while not self._begin:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                elif event.type == pg.JOYBUTTONDOWN:
                    if event.button == GAMEPAD["BTN_A"]:
                        # easy mode
                        ball.initial_speed_factor = BALL_SPEED["EASY"]
                        return True
                    elif event.button == GAMEPAD["BTN_B"]:
                        # normal mode
                        ball.initial_speed_factor = BALL_SPEED["NORMAL"]
                        return True
                    elif event.button == GAMEPAD["BTN_X"]:
                        # expert mode
                        ball.initial_speed_factor = BALL_SPEED["EXPERT"]
                        return True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    elif event.key == pg.K_a:
                        # easy mode
                        ball.initial_speed_factor = BALL_SPEED["EASY"]
                        return True
                    elif event.key == pg.K_b:
                        # normal mode
                        ball.initial_speed_factor = BALL_SPEED["NORMAL"]
                        return True
                    elif event.key == pg.K_x:
                        # expert mode
                        ball.initial_speed_factor = BALL_SPEED["EXPERT"]
                        return True

            if self._begin:
                # reset all parameters to restart the game
                screen.fill(COLORS["BLACK"])

            pg.display.flip()

        # reset restart flag when self._restart = True and the while ends
        self._begin = False

    def gameover(self, screen, player):
        """Display Game Over screen"""
        if self._game_mode == MODES["ONE_PLAYER"]:
            if player == CLASSICAL_COMPUTER:

                screen.fill(COLORS["BLACK"])

                gameover_text = "Game Over"
                text = FONTS["GAMEOVER"].render(gameover_text, 1, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
                screen.blit(text, text_pos)

                gameover_text = "Classical computer"
                text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
                screen.blit(text, text_pos)

                gameover_text = "still rules the world"
                text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
                screen.blit(text, text_pos)

                self.credits(screen)

            if player == QUANTUM_COMPUTER_1P:

                screen.fill(COLORS["BLACK"])

                gameover_text = "Congratulations!"
                text = FONTS["GAMEOVER"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
                screen.blit(text, text_pos)

                gameover_text = "You demonstrated quantum supremacy"
                text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
                screen.blit(text, text_pos)

                gameover_text = "for the first time in human history!"
                text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
                screen.blit(text, text_pos)

                self.credits(screen)
        else:
            if player == QUANTUM_COMPUTER_1P:

                screen.fill(COLORS["BLACK"])

                gameover_text = "Game Over"
                text = FONTS["GAMEOVER"].render(gameover_text, 1, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
                screen.blit(text, text_pos)

                gameover_text = "Player 1"
                text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
                screen.blit(text, text_pos)

                gameover_text = "wins!"
                text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
                screen.blit(text, text_pos)

                self.credits(screen)

            if player == QUANTUM_COMPUTER_2P:
                screen.fill(COLORS["BLACK"])

                gameover_text = "Player 2"
                text = FONTS["GAMEOVER"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
                screen.blit(text, text_pos)

                gameover_text = "wins!"
                text = FONTS["REPLAY"].render(gameover_text, 5, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
                screen.blit(text, text_pos)

                self.credits(screen)

    def dashed_line(self, screen):
        for i in range(
            10, round(WINDOW_HEIGHT * 0.7), 2 * WIDTH_UNIT
        ):  # draw dashed line
            pg.draw.rect(
                screen,
                COLORS["GRAY"],
                (WINDOW_WIDTH // 2 - 5, i, 0.5 * WIDTH_UNIT, WIDTH_UNIT),
                0,
            )

    def score(self, players, screen):
        # Print the score
        text = FONTS["PLAYER"].render(
            "Classical Computer"
            if players[0].player_type == CLASSICAL_COMPUTER
            else "Quantum Computer",
            1,
            COLORS["GRAY"],
        )
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.75) - WIDTH_UNIT * 4.5, WIDTH_UNIT * 1.5)
        )
        screen.blit(text, text_pos)

        text = FONTS["PLAYER"].render(
            "Classical Computer"
            if players[1].player_type == CLASSICAL_COMPUTER
            else "Quantum Computer",
            1,
            COLORS["GRAY"],
        )
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.25) + WIDTH_UNIT * 4.5, WIDTH_UNIT * 1.5)
        )
        screen.blit(text, text_pos)

        score_print = str(players[0].score)
        text = FONTS["SCORE"].render(score_print, 1, COLORS["GRAY"])
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.75) - WIDTH_UNIT * 4.5, WIDTH_UNIT * 8)
        )
        screen.blit(text, text_pos)

        score_print = str(players[1].score)
        text = FONTS["SCORE"].render(score_print, 1, COLORS["GRAY"])
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.25) + WIDTH_UNIT * 4.5, WIDTH_UNIT * 8)
        )
        screen.blit(text, text_pos)

    def credits(self, screen):
        credit_text = "Credits"
        text = FONTS["CREDIT"].render(credit_text, 1, COLORS["WHITE"])
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 8)
        )
        screen.blit(text, text_pos)

        credit_text = (
            "Made by Huang Junye, James Weaver, Jarrod Reilly and Anastasia Jeffery"
        )
        text = FONTS["CREDIT"].render(credit_text, 1, COLORS["WHITE"])
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 5)
        )
        screen.blit(text, text_pos)

        credit_text = "Initiated at IBM Qiskit Camp 2019"
        text = FONTS["CREDIT"].render(credit_text, 1, COLORS["WHITE"])
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 3)
        )
        screen.blit(text, text_pos)

        credit_text = "Powered by JavaFXpert/quantum-circuit-game"
        text = FONTS["CREDIT"].render(credit_text, 1, COLORS["WHITE"])
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 1)
        )
        screen.blit(text, text_pos)

    def replay(self, screen, players):
        """Pause the game and ask if the player wants to play again"""
        blink_time = pg.time.get_ticks()

        while not self._restart:
            for event in pg.event.get():
                if event.type != pg.QUIT:
                    self._restart = True

            if self._restart:
                for player in players:
                    # reset all parameters to restart the game
                    player.reset_score()

                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.circuit_grid_model.reset_circuit()
                        player.circuit_grid.update()
                        player.circuit_grid.reset_cursor()

            # Make blinking text
            if pg.time.get_ticks() - blink_time > 1000:
                blink_time = pg.time.get_ticks()
            if pg.time.get_ticks() - blink_time > 500:
                replay_text = "Press Any Key to Play Again"
                text = FONTS["REPLAY"].render(replay_text, 1, COLORS["WHITE"])
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
                screen.blit(text, text_pos)
                pg.display.flip()
            else:
                # show a black box to blink the text every 0.5s
                pg.draw.rect(
                    screen,
                    COLORS["BLACK"],
                    (
                        WIDTH_UNIT * 10,
                        WIDTH_UNIT * 35,
                        WIDTH_UNIT * 80,
                        WIDTH_UNIT * 10,
                    ),
                )
                pg.display.flip()

        # reset restart flag when self._restart = True and the while ends
        self._restart = False
