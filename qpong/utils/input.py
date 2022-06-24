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
Quantum player input events and control
"""

import numpy as np

import pygame

from qpong.utils import gamepad
from qpong.utils.navigation import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT


class Input:
    """
    Handle input events
    """

    def __init__(self):
        self.running = True
        pygame.init()
        pygame.joystick.init()
        self.num_joysticks = pygame.joystick.get_count()
        if self.num_joysticks > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self.gamepad_repeat_delay = 200
        self.gamepad_neutral = True
        self.gamepad_pressed_timer = 0
        self.gamepad_last_update = pygame.time.get_ticks()

    def handle_input(self, level, screen, scene):
        # pylint: disable=too-many-branches disable=too-many-statements
        """
        Handle quantum player input
        """

        gamepad_move = False
        circuit_grid = level.circuit_grid

        # use joystick if it's connected
        if self.num_joysticks > 0:
            joystick_hat = self.joystick.get_hat(0)

            if joystick_hat == (0, 0):
                self.gamepad_neutral = True
                self.gamepad_pressed_timer = 0
            else:
                if self.gamepad_neutral:
                    gamepad_move = True
                    self.gamepad_neutral = False
                else:
                    self.gamepad_pressed_timer += (
                        pygame.time.get_ticks() - self.gamepad_last_update
                    )
            if self.gamepad_pressed_timer > self.gamepad_repeat_delay:
                gamepad_move = True
                self.gamepad_pressed_timer -= self.gamepad_repeat_delay
            if gamepad_move:
                if joystick_hat == (-1, 0):
                    self.move_update_circuit_grid_display(
                        screen, circuit_grid, MOVE_LEFT
                    )
                elif joystick_hat == (1, 0):
                    self.move_update_circuit_grid_display(
                        screen, circuit_grid, MOVE_RIGHT
                    )
                elif joystick_hat == (0, 1):
                    self.move_update_circuit_grid_display(screen, circuit_grid, MOVE_UP)
                elif joystick_hat == (0, -1):
                    self.move_update_circuit_grid_display(
                        screen, circuit_grid, MOVE_DOWN
                    )
            self.gamepad_last_update = pygame.time.get_ticks()

            # Check left thumbstick position
            # left_thumb_x = self.joystick.get_axis(0)
            # left_thumb_y = self.joystick.get_axis(1)

        # Handle Input Events
        for event in pygame.event.get():
            pygame.event.pump()

            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == gamepad.BTN_A:
                    # Place X gate
                    circuit_grid.handle_input_x()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.button == gamepad.BTN_X:
                    # Place Y gate
                    circuit_grid.handle_input_y()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.button == gamepad.BTN_B:
                    # Place Z gate
                    circuit_grid.handle_input_z()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.button == gamepad.BTN_Y:
                    # Place Hadamard gate
                    circuit_grid.handle_input_h()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.button == gamepad.BTN_RIGHT_TRIGGER:
                    # Delete gate
                    circuit_grid.handle_input_delete()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.button == gamepad.BTN_RIGHT_THUMB:
                    # Add or remove a control
                    circuit_grid.handle_input_ctrl()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.button == gamepad.BTN_LEFT_BUMPER:
                    # Update visualizations
                    self.update_paddle(level, screen, scene)

            elif event.type == pygame.JOYAXISMOTION:
                # print("event: ", event)
                if (
                    event.axis == gamepad.AXIS_RIGHT_THUMB_X
                    and self.joystick.get_axis(gamepad.AXIS_RIGHT_THUMB_X) >= 0.95
                ):
                    circuit_grid.handle_input_rotate(np.pi / 8)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                if (
                    event.axis == gamepad.AXIS_RIGHT_THUMB_X
                    and self.joystick.get_axis(gamepad.AXIS_RIGHT_THUMB_X) <= -0.95
                ):
                    circuit_grid.handle_input_rotate(-np.pi / 8)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                if (
                    event.axis == gamepad.AXIS_RIGHT_THUMB_Y
                    and self.joystick.get_axis(gamepad.AXIS_RIGHT_THUMB_Y) <= -0.95
                ):
                    circuit_grid.handle_input_move_ctrl(MOVE_UP)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                if (
                    event.axis == gamepad.AXIS_RIGHT_THUMB_Y
                    and self.joystick.get_axis(gamepad.AXIS_RIGHT_THUMB_Y) >= 0.95
                ):
                    circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_a:
                    circuit_grid.move_to_adjacent_node(MOVE_LEFT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_d:
                    circuit_grid.move_to_adjacent_node(MOVE_RIGHT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_w:
                    circuit_grid.move_to_adjacent_node(MOVE_UP)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_s:
                    circuit_grid.move_to_adjacent_node(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_x:
                    circuit_grid.handle_input_x()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_y:
                    circuit_grid.handle_input_y()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_z:
                    circuit_grid.handle_input_z()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_h:
                    circuit_grid.handle_input_h()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_SPACE:
                    circuit_grid.handle_input_delete()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_c:
                    # Add or remove a control
                    circuit_grid.handle_input_ctrl()
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_UP:
                    # Move a control qubit up
                    circuit_grid.handle_input_move_ctrl(MOVE_UP)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_DOWN:
                    # Move a control qubit down
                    circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_LEFT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(-np.pi / 8)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_RIGHT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(np.pi / 8)
                    circuit_grid.draw(screen)
                    self.update_paddle(level, screen, scene)
                    pygame.display.flip()
                elif event.key == pygame.K_TAB:
                    # Update visualizations
                    self.update_paddle(level, screen, scene)

    @staticmethod
    def update_paddle(level, screen, scene):
        """
        Update state vector paddle
        """
        # Update visualizations

        circuit_grid_model = level.circuit_grid_model
        right_statevector = level.right_statevector
        circuit_grid = level.circuit_grid
        statevector_grid = level.statevector_grid

        circuit = circuit_grid_model.construct_circuit()
        statevector_grid.paddle_before_measurement(circuit, scene.qubit_num, 100)
        right_statevector.arrange()
        circuit_grid.draw(screen)
        pygame.display.flip()

    @staticmethod
    def move_update_circuit_grid_display(screen, circuit_grid, direction):
        """
        Update circuit grid after move
        """
        circuit_grid.move_to_adjacent_node(direction)
        circuit_grid.draw(screen)
        pygame.display.flip()
