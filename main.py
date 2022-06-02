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
#
"""Quantum version of the classic Pong game"""

import random

import pygame as pg
from pygame import DOUBLEBUF, FULLSCREEN, HWSURFACE

from components.ball import Ball
from components.scene import Scene
from components.player import Player

from prepare import (
    CLASSICAL_COMPUTER,
    QUANTUM_COMPUTER_1P,
    QUANTUM_COMPUTER_2P,
    WIDTH_UNIT,
    WINDOW_HEIGHT,
    WINDOW_SIZE,
    COLORS,
    MODES,
    POSITIONS,
    BALL_ACTIONS,
    WIN_SCORE,
    QUBIT_NUM,
    FONTS,
)
from utils.input import Input

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")


def main():
    # hardware acceleration to reduce flickering. Works only in full screen
    flags = DOUBLEBUF | HWSURFACE | FULLSCREEN
    screen = pg.display.set_mode(WINDOW_SIZE, flags)

    # Display until loading finishes.
    screen.fill(COLORS["BLACK"])
    _render = FONTS["GAMEOVER"].render("LOADING...", 0, pg.Color("white"))
    SCREEN_RECT = pg.Rect((0, 0), WINDOW_SIZE)
    screen.blit(_render, _render.get_rect(center=SCREEN_RECT.center))

    pg.display.set_caption("QPong")

    # clock for timing
    clock = pg.time.Clock()
    old_clock = pg.time.get_ticks()

    # initialize scene, level and input Classes
    scene = Scene(QUBIT_NUM)

    # players
    players = []

    input = Input()

    # define ball
    ball = Ball()
    balls = (
        pg.sprite.Group()
    )  # sprite group type is needed for sprite collide function in pg

    balls.add(ball)

    # Show start screen to select difficulty
    input.running = scene.mode(screen)  # start screen returns running flag
    if not input.running:
        pg.quit()
        return

    input.running = scene.difficulty(screen, ball)  # start mode selections returns flag
    if not input.running:
        pg.quit()
        return

    if scene.game_mode == MODES["ONE_PLAYER"]:
        players += [
            Player(QUBIT_NUM, POSITIONS["RIGHT"], QUANTUM_COMPUTER_1P, scene.game_mode)
        ]
        players += [
            Player(QUBIT_NUM, POSITIONS["LEFT"], CLASSICAL_COMPUTER, scene.game_mode)
        ]
    elif scene.game_mode == MODES["TWO_PLAYER"]:
        players += [
            Player(QUBIT_NUM, POSITIONS["RIGHT"], QUANTUM_COMPUTER_1P, scene.game_mode)
        ]
        players += [
            Player(QUBIT_NUM, POSITIONS["LEFT"], QUANTUM_COMPUTER_2P, scene.game_mode)
        ]

    # Put all moving sprites a group so that they can be drawn together
    moving_sprites = pg.sprite.Group()
    moving_sprites.add(ball)
    for player in players:
        moving_sprites.add(player.paddle)

    # update the screen
    pg.display.flip()

    # reset the ball
    ball.reset()

    # a valuable to record the time when the paddle is measured
    measure_time = 100000

    # Main Loop
    while input.running:
        # set maximum frame rate
        clock.tick(60)

        # refill whole screen with black color at each frame
        screen.fill(COLORS["BLACK"])

        ball.update()  # update ball position
        scene.dashed_line(screen)  # draw dashed line in the middle of the screen
        scene.score(players, screen)  # print score

        for _, player in enumerate(players):
            if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                player.statevector.draw(
                    screen
                )  # draw right paddle together with statevector grid
                player.circuit_grid.draw(screen)  # draw circuit grid
                moving_sprites.draw(screen)  # draw moving sprites

                # Show game over screen if the score reaches WIN_SCORE, reset everything if replay == TRUE
                if player.score >= WIN_SCORE:
                    input.running = scene.gameover(screen, player.player_type)
                    scene.replay(screen, players)

                    player.update_paddle(screen)

                if player.score >= WIN_SCORE:
                    input.running = scene.gameover(screen, player.player_type)
                    scene.replay(screen, players)

                    player.update_paddle(screen)

        # computer paddle movement
        if scene.game_mode == MODES["ONE_PLAYER"]:
            cpu_player = next(
                filter(lambda p: p.player_type == CLASSICAL_COMPUTER, players)
            )
            qcpu_player = next(
                filter(
                    lambda p: p.player_type
                    in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P),
                    players,
                )
            )

            if cpu_player:
                if pg.time.get_ticks() - old_clock > 300:
                    cpu_player.paddle.rect.y = (
                        ball.y
                        - qcpu_player.statevector_grid.block_size / 2
                        + random.randint(-WIDTH_UNIT * 4, WIDTH_UNIT * 4)
                    )
                    old_clock = pg.time.get_ticks()

            # handle input events
            input.handle_input(players, screen)

            # check ball location and decide what to do
            ball.action(players)

            if ball.ball_action == BALL_ACTIONS["MEASURE_RIGHT"]:
                circuit = qcpu_player.circuit_grid_model.compute_circuit()
                pos = qcpu_player.statevector_grid.paddle_after_measurement(
                    qcpu_player.position, circuit, QUBIT_NUM, 1
                )
                qcpu_player.statevector.arrange()

                # paddle after measurement
                qcpu_player.paddle.rect.y = (
                    pos * round(WINDOW_HEIGHT * 0.7) / (2**QUBIT_NUM)
                )
                measure_time = pg.time.get_ticks()

            if pg.sprite.spritecollide(qcpu_player.paddle, balls, False):
                ball.bounce_edge()

            if pg.sprite.spritecollide(cpu_player.paddle, balls, False):
                ball.bounce_edge()

            if pg.time.get_ticks() - measure_time > 400:
                # refresh the screen a moment after measurement to update visual
                qcpu_player.update_paddle(screen)
                # add a buffer time before measure again
                measure_time = pg.time.get_ticks() + 100000

        elif scene.game_mode == MODES["TWO_PLAYER"]:
            # handle input events
            input.handle_input(players, screen)

            # check ball location and decide what to do
            ball.action(players)

            if ball.ball_action == BALL_ACTIONS["MEASURE_RIGHT"]:
                circuit = players[0].circuit_grid_model.compute_circuit()
                pos = players[0].statevector_grid.paddle_after_measurement(
                    players[0].position, circuit, QUBIT_NUM, 1
                )
                players[0].statevector.arrange()

                # paddle after measurement
                players[0].paddle.rect.y = (
                    pos * round(WINDOW_HEIGHT * 0.7) / (2**QUBIT_NUM)
                )
                measure_time = pg.time.get_ticks()

            if ball.ball_action == BALL_ACTIONS["MEASURE_LEFT"]:
                circuit = players[1].circuit_grid_model.compute_circuit()
                pos = players[1].statevector_grid.paddle_after_measurement(
                    players[1].position, circuit, QUBIT_NUM, 1
                )
                players[1].statevector.arrange()

                # paddle after measurement
                players[1].paddle.rect.y = (
                    pos * round(WINDOW_HEIGHT * 0.7) / (2**QUBIT_NUM)
                )
                measure_time = pg.time.get_ticks()

            if pg.sprite.spritecollide(players[0].paddle, balls, False):
                ball.bounce_edge()

            if pg.sprite.spritecollide(players[1].paddle, balls, False):
                ball.bounce_edge()

            if pg.time.get_ticks() - measure_time > 400:
                # refresh the screen a moment after measurement to update visual
                players[0].update_paddle(screen)
                players[1].update_paddle(screen)
                # add a buffer time before measure again
                measure_time = pg.time.get_ticks() + 100000

        # Update the screen
        if input.running:
            pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
