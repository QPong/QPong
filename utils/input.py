import numpy as np
import pygame as pg

from prepare import GAMEPAD, MOVES, QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P


class Input(object):
    """Handle input events"""

    def __init__(self):
        pg.joystick.init()

        self._running = True
        self._joysticks = []
        self._num_joysticks = pg.joystick.get_count()

        if self._num_joysticks > 0:
            for j in range(0, min(2, self._num_joysticks)):
                self._joysticks += [pg.joystick.Joystick(j)]
                self._joysticks[j].init()

        self._gamepad_repeat_delay = 200
        self._gamepad_neutral = True
        self._gamepad_pressed_timer = 0
        self._gamepad_last_update = pg.time.get_ticks()

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    def handle_input(self, players, screen):
        gamepad_move = False

        # use joystick if it's connected
        if self._num_joysticks > 0:
            for j in range(0, min(2, self._num_joysticks)):
                joystick_hat = self._joysticks[j].get_hat(0)

                if joystick_hat == (0, 0):
                    self._gamepad_neutral = True
                    self._gamepad_pressed_timer = 0
                else:
                    if self._gamepad_neutral:
                        gamepad_move = True
                        self._gamepad_neutral = False
                    else:
                        self._gamepad_pressed_timer += (
                            pg.time.get_ticks() - self._gamepad_last_update
                        )

                if self._gamepad_pressed_timer > self._gamepad_repeat_delay:
                    gamepad_move = True
                    self._gamepad_pressed_timer -= self._gamepad_repeat_delay

                if gamepad_move:
                    if joystick_hat == (-1, 0):
                        players[j].move_update_circuit_grid_display(
                            screen, MOVES["LEFT"]
                        )
                    elif joystick_hat == (1, 0):
                        players[j].move_update_circuit_grid_display(
                            screen, MOVES["RIGHT"]
                        )
                    elif joystick_hat == (0, 1):
                        players[j].move_update_circuit_grid_display(screen, MOVES["UP"])
                    elif joystick_hat == (0, -1):
                        players[j].move_update_circuit_grid_display(
                            screen, MOVES["DOWN"]
                        )
                self._gamepad_last_update = pg.time.get_ticks()

            # Check left thumbstick position
            # left_thumb_x = self._joystick.get_axis(0)
            # left_thumb_y = self._joystick.get_axis(1)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
                pg.quit()
            elif event.type == pg.JOYBUTTONDOWN:
                if event.button == GAMEPAD["BTN_A"]:
                    # TODO: Check if quantum player
                    player = players[min(1, event.joy)]
                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.circuit_grid.handle_input_x()
                        player.circuit_grid.draw(screen)
                        player.update_paddle(screen)
                        pg.display.flip()
                elif event.button == GAMEPAD["BTN_X"]:
                    # Place Y gate
                    player = players[min(1, event.joy)]
                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.circuit_grid.handle_input_y()
                        player.circuit_grid.draw(screen)
                        player.update_paddle(screen)
                        pg.display.flip()
                elif event.button == GAMEPAD["BTN_B"]:
                    # Place Z gate
                    player = players[min(1, event.joy)]
                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.circuit_grid.handle_input_z()
                        player.circuit_grid.draw(screen)
                        player.update_paddle(screen)
                        pg.display.flip()
                elif event.button == GAMEPAD["BTN_Y"]:
                    # Place Hadamard gate
                    player = players[min(1, event.joy)]
                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.circuit_grid.handle_input_h()
                        player.circuit_grid.draw(screen)
                        player.update_paddle(screen)
                        pg.display.flip()
                elif event.button == GAMEPAD["BTN_RIGHT_TRIGGER"]:
                    # Delete gate
                    player = players[min(1, event.joy)]
                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.circuit_grid.handle_input_delete()
                        player.circuit_grid.draw(screen)
                        player.update_paddle(screen)
                        pg.display.flip()
                elif event.button == GAMEPAD["BTN_RIGHT_THUMB"]:
                    # Add or remove a control
                    player = players[min(1, event.joy)]
                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.circuit_grid.handle_input_ctrl()
                        player.circuit_grid.draw(screen)
                        player.update_paddle(screen)
                        pg.display.flip()
                elif event.button == GAMEPAD["BTN_LEFT_BUMPER"]:
                    # Update visualizations
                    # TODO: Refactor following code into methods, etc.
                    player = players[min(1, event.joy)]
                    if player.player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
                        player.update_paddle(screen)
                        pg.display.flip()

            elif event.type == pg.JOYAXISMOTION:
                # print("event: ", event)
                for j in range(0, min(2, self._num_joysticks)):
                    if (
                        event.axis == GAMEPAD["AXIS_RIGHT_THUMB_X"]
                        and self._joysticks[j].get_axis(GAMEPAD["AXIS_RIGHT_THUMB_X"])
                        >= 0.95
                    ):

                        player = players[min(1, event.joy)]

                        if player.player_type in (
                            QUANTUM_COMPUTER_1P,
                            QUANTUM_COMPUTER_2P,
                        ):
                            player.circuit_grid.handle_input_rotate(np.pi / 8)
                            player.circuit_grid.draw(screen)
                            player.update_paddle(screen)
                            pg.display.flip()
                    if (
                        event.axis == GAMEPAD["AXIS_RIGHT_THUMB_X"]
                        and self._joysticks[j].get_axis(GAMEPAD["AXIS_RIGHT_THUMB_X"])
                        <= -0.95
                    ):

                        player = players[min(1, event.joy)]

                        if player.player_type in (
                            QUANTUM_COMPUTER_1P,
                            QUANTUM_COMPUTER_2P,
                        ):
                            player.circuit_grid.handle_input_rotate(-np.pi / 8)
                            player.circuit_grid.draw(screen)
                            player.update_paddle(screen)
                            pg.display.flip()
                    if (
                        event.axis == GAMEPAD["AXIS_RIGHT_THUMB_Y"]
                        and self._joysticks[j].get_axis(GAMEPAD["AXIS_RIGHT_THUMB_Y"])
                        <= -0.95
                    ):
                        player = players[min(1, event.joy)]
                        if player.player_type in (
                            QUANTUM_COMPUTER_1P,
                            QUANTUM_COMPUTER_2P,
                        ):
                            player.circuit_grid.handle_input_move_ctrl(MOVES["UP"])
                            player.circuit_grid.draw(screen)
                            player.update_paddle(screen)
                            pg.display.flip()
                    if (
                        event.axis == GAMEPAD["AXIS_RIGHT_THUMB_Y"]
                        and self._joysticks[j].get_axis(GAMEPAD["AXIS_RIGHT_THUMB_Y"])
                        >= 0.95
                    ):
                        player = players[min(1, event.joy)]
                        if player.player_type in (
                            QUANTUM_COMPUTER_1P,
                            QUANTUM_COMPUTER_2P,
                        ):
                            player.circuit_grid.handle_input_move_ctrl(MOVES["DOWN"])
                            player.circuit_grid.draw(screen)
                            player.update_paddle(screen)
                            pg.display.flip()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._running = False
                    pg.quit()
                elif event.key == pg.K_a:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.move_to_adjacent_node(MOVES["LEFT"])
                        players[0].circuit_grid.draw(screen)
                        pg.display.flip()
                elif event.key == pg.K_d:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.move_to_adjacent_node(MOVES["RIGHT"])
                        players[0].circuit_grid.draw(screen)
                        pg.display.flip()
                elif event.key == pg.K_w:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.move_to_adjacent_node(MOVES["UP"])
                        players[0].circuit_grid.draw(screen)
                        pg.display.flip()
                elif event.key == pg.K_s:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.move_to_adjacent_node(MOVES["DOWN"])
                        players[0].circuit_grid.draw(screen)
                        pg.display.flip()
                elif event.key == pg.K_r:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.handle_input_x()
                        players[0].circuit_grid.draw(screen)
                        players[0].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_t:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.handle_input_y()
                        players[0].circuit_grid.draw(screen)
                        players[0].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_y:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.handle_input_z()
                        players[0].circuit_grid.draw(screen)
                        players[0].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_u:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.handle_input_h()
                        players[0].circuit_grid.draw(screen)
                        players[0].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_i:
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.handle_input_delete()
                        players[0].circuit_grid.draw(screen)
                        players[0].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_o:
                    # Add or remove a control
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].circuit_grid.handle_input_ctrl()
                        players[0].circuit_grid.draw(screen)
                        players[0].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_UP:
                    # Move a control qubit up
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.move_to_adjacent_node(MOVES["UP"])
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_DOWN:
                    # Move a control qubit down
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.move_to_adjacent_node(MOVES["DOWN"])
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_LEFT:
                    # Rotate a gate
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.move_to_adjacent_node(MOVES["LEFT"])
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_RIGHT:
                    # Rotate a gate
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.move_to_adjacent_node(MOVES["RIGHT"])
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_v:
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.handle_input_x()
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_b:
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.handle_input_y()
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_n:
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.handle_input_z()
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_m:
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.handle_input_h()
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_COMMA:
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.handle_input_delete()
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_PERIOD:
                    # Add or remove a control
                    if players[1].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[1].circuit_grid.handle_input_ctrl()
                        players[1].circuit_grid.draw(screen)
                        players[1].update_paddle(screen)
                        pg.display.flip()
                elif event.key == pg.K_TAB:
                    # Update visualizations
                    # TODO: Refactor following code into methods, etc.
                    if players[0].player_type in (
                        QUANTUM_COMPUTER_1P,
                        QUANTUM_COMPUTER_2P,
                    ):
                        players[0].update_paddle(screen)
