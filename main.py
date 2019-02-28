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
# TODO: Create viz that displays generated Qiskit code for circuit
# TODO: Prevent error from occurring when circuit is empty
#
"""Create quantum circuits with Qiskit and Pygame"""

import pygame
from pygame.locals import *

from model.circuit_grid_model import *
from model import circuit_node_types as node_types
from containers.vbox import VBox
from utils.colors import WHITE
from utils.navigation import *
from utils.gamepad import *
from viz.circuit_diagram import CircuitDiagram
from viz.measurements_histogram import MeasurementsHistogram
from viz.qsphere import QSphere
from viz.statevector_grid import StatevectorGrid
from viz.statevector_grid_1 import StatevectorGrid1
from viz.unitary_grid import UnitaryGrid
from controls.circuit_grid import *
from controls.ball_screen import *
from utils.ball import *
from utils.removeball import *
from utils.measurement import *

WINDOW_WIDTH=1200
WINDOW_HEIGHT=1000
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

pygame.init()

pygame.joystick.init()
num_joysticks = pygame.joystick.get_count()
if num_joysticks > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

screen = pygame.display.set_mode(WINDOW_SIZE)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)

pygame.font.init()

QUBIT_NUM=3


def main():
    pygame.display.set_caption('QPong')

    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare objects
    clock = pygame.time.Clock()

    circuit_grid_model = CircuitGridModel(QUBIT_NUM, 18)

    circuit_grid_model.set_node(0, 0, CircuitGridNode(node_types.IDEN))

    circuit = circuit_grid_model.compute_circuit()


    circuit_diagram = CircuitDiagram(circuit)
    unitary_grid = UnitaryGrid(circuit)
    # histogram = MeasurementsHistogram(circuit)
    # qsphere = QSphere(circuit)
    statevector_grid = StatevectorGrid(circuit, QUBIT_NUM, 100)
    statevector_grid_1 = StatevectorGrid1(circuit)

    # left_sprites = VBox(0, 0, circuit_diagram, qsphere)
    #left_sprites = VBox(0, 0, qsphere)
    # middle_sprites = VBox(600, 100, histogram, unitary_grid)
    # middle_sprites = VBox(600, 100, histogram)

    right_sprites = VBox(WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0, statevector_grid)
    left_sprite_computer = VBox(0,0, statevector_grid_1)

    circuit_grid = CircuitGrid(10, WINDOW_HEIGHT*0.55, circuit_grid_model)
    ball_screen = BallScreen(0, 0)
    screen.blit(background, (0, 0))

    # pygame.display.flip()



    # screen.blit(background, (0, 0))
    #left_sprites.draw(screen)
    #middle_sprites.draw(screen)
    circuit_grid.draw(screen)
    ball_screen.draw(screen)
    right_sprites.draw(screen)
    left_sprite_computer.draw(screen)


    ball = Ball()
    removeball = RemoveBall(ball.x, ball.y)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(removeball)
    movingsprites.add(ball)

    #movingsprites.draw(screen)

    ball.ball_reset()
    pygame.display.flip()

    gamepad_repeat_delay = 100
    gamepad_neutral = True
    gamepad_pressed_timer = 0
    gamepad_last_update = pygame.time.get_ticks()

    # Main Loop
    going = True
    while going:
        clock.tick(30)

        pygame.time.wait(10)
        #screen.fill(BLACK)
        removeball.update(ball.get_xpos(), ball.get_ypos())
        ball.update()

        # computer measurement

        movingsprites.add(ball)
        movingsprites.draw(screen)
        pygame.display.flip()

        gamepad_move = False
        joystick_hat = joystick.get_hat(0)

        if joystick_hat == (0, 0):
            gamepad_neutral = True
            gamepad_pressed_timer = 0
        else:
            if gamepad_neutral:
                gamepad_move = True
                gamepad_neutral = False
            else:
                gamepad_pressed_timer += pygame.time.get_ticks() - gamepad_last_update
        if gamepad_pressed_timer > gamepad_repeat_delay:
            gamepad_move = True
            gamepad_pressed_timer -= gamepad_repeat_delay
        if gamepad_move:
            if joystick_hat == (-1, 0):
                move_update_circuit_grid_display(circuit_grid, MOVE_LEFT)
            elif joystick_hat == (1, 0):
                move_update_circuit_grid_display(circuit_grid, MOVE_RIGHT)
            elif joystick_hat == (0, 1):
                move_update_circuit_grid_display(circuit_grid, MOVE_UP)
            elif joystick_hat == (0, -1):
                move_update_circuit_grid_display(circuit_grid, MOVE_DOWN)
        gamepad_last_update = pygame.time.get_ticks()

        # Check left thumbstick position
        left_thumb_x = joystick.get_axis(0)
        left_thumb_y = joystick.get_axis(1)

        # Handle Input Events
        for event in pygame.event.get():
            pygame.event.pump()

            # if event.type != MOUSEMOTION:
            #     print("event: ", event)
            if event.type == QUIT:
                going = False

            elif event.type == JOYBUTTONDOWN:
                if event.button == BTN_A:
                    # Place X gate
                    circuit_grid.handle_input_x()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.button == BTN_X:
                    # Place Y gate
                    circuit_grid.handle_input_y()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.button == BTN_B:
                    # Place Z gate
                    circuit_grid.handle_input_z()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.button == BTN_Y:
                    # Place Hadamard gate
                    circuit_grid.handle_input_h()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.button == BTN_RIGHT_TRIGGER:
                    # Delete gate
                    circuit_grid.handle_input_delete()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.button == BTN_RIGHT_THUMB:
                    # Add or remove a control
                    circuit_grid.handle_input_ctrl()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.button == BTN_LEFT_BUMPER:
                    # Update visualizations
                    # TODO: Refactor following code into methods, etc.
                    screen.blit(background, (0, 0))
                    circuit = circuit_grid_model.compute_circuit()
                    circuit_diagram.set_circuit(circuit)
                    unitary_grid.set_circuit(circuit)
                    # qsphere.set_circuit(circuit)
                     # histogram.set_circuit(circuit)
                    statevector_grid.set_circuit(circuit, QUBIT_NUM, 100)
                    # left_sprites.arrange()
                    # middle_sprites.arrange()
                    right_sprites.arrange()
                    left_sprite_computer.arrange()
                    # left_sprites.draw(screen)
                    # middle_sprites.draw(screen)
                    ball_screen.draw(screen)
                    right_sprites.draw(screen)
                    left_sprite_computer.draw(screen)
                    circuit_grid.draw(screen)
                    pygame.display.flip()

            elif event.type == JOYAXISMOTION:
                # print("event: ", event)
                if event.axis == AXIS_RIGHT_THUMB_X and joystick.get_axis(AXIS_RIGHT_THUMB_X) >= 0.95:
                    circuit_grid.handle_input_rotate(np.pi / 8)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                if event.axis == AXIS_RIGHT_THUMB_X and joystick.get_axis(AXIS_RIGHT_THUMB_X) <= -0.95:
                    circuit_grid.handle_input_rotate(-np.pi / 8)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                if event.axis == AXIS_RIGHT_THUMB_Y and joystick.get_axis(AXIS_RIGHT_THUMB_Y) <= -0.95:
                    circuit_grid.handle_input_move_ctrl(MOVE_UP)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                if event.axis == AXIS_RIGHT_THUMB_Y and joystick.get_axis(AXIS_RIGHT_THUMB_Y) >= 0.95:
                    circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    pygame.display.flip()

            elif event.type == KEYDOWN:
                index_increment = 0
                if event.key == K_ESCAPE:
                    going = False
                elif event.key == K_a:
                    circuit_grid.move_to_adjacent_node(MOVE_LEFT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_d:
                    circuit_grid.move_to_adjacent_node(MOVE_RIGHT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_w:
                    circuit_grid.move_to_adjacent_node(MOVE_UP)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_s:
                    circuit_grid.move_to_adjacent_node(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_x:
                    circuit_grid.handle_input_x()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_y:
                    circuit_grid.handle_input_y()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_z:
                    circuit_grid.handle_input_z()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_h:
                    circuit_grid.handle_input_h()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_BACKSLASH:
                    circuit_grid.handle_input_delete()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_c:
                    # Add or remove a control
                    circuit_grid.handle_input_ctrl()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_UP:
                    # Move a control qubit up
                    circuit_grid.handle_input_move_ctrl(MOVE_UP)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_DOWN:
                    # Move a control qubit down
                    circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_LEFT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(-np.pi/8)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_RIGHT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(np.pi / 8)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_SPACE:
                    # Update visualizations
                    # TODO: Refactor following code into methods, etc.
                    screen.blit(background, (0, 0))
                    circuit = circuit_grid_model.compute_circuit()
                    circuit_diagram.set_circuit(circuit)
                    unitary_grid.set_circuit(circuit)
                    # qsphere.set_circuit(circuit)
                    # histogram.set_circuit(circuit)
                    statevector_grid.set_circuit(circuit, QUBIT_NUM, 100)
                    # left_sprites.arrange()
                    # middle_sprites.arrange()
                    right_sprites.arrange()
                    left_sprite_computer.arrange()
                    # left_sprites.draw(screen)
                    # middle_sprites.draw(screen)
                    right_sprites.draw(screen)
                    left_sprite_computer.draw(screen)
                    circuit_grid.draw(screen)
                    pygame.display.flip()

            # measurement process

        # player measurement
        if ball.if_edge() == 2:
            circuit = circuit_grid_model.compute_circuit()
            circuit_diagram.set_circuit(circuit)
            unitary_grid.set_circuit(circuit)
            statevector_grid.set_circuit_measure(circuit, QUBIT_NUM, 1)
            right_sprites.arrange()
            left_sprite_computer.arrange()
            right_sprites.draw(screen)
            left_sprite_computer.draw(screen)
            circuit_grid.draw(screen)
            pygame.display.flip()

            # else:
            #     print("event: ", event)

    pygame.quit()


def move_update_circuit_grid_display(circuit_grid, direction):
    circuit_grid.move_to_adjacent_node(direction)
    circuit_grid.draw(screen)
    pygame.display.flip()


if __name__ == '__main__':
    main()
