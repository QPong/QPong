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
# TODO: Use the convert() method to improve performance?
#
"""Create quantum circuits with Qiskit and Pygame"""

import pygame
from pygame.locals import *

from model.circuit_grid_model import *
from model import circuit_node_types as node_types
from containers.vbox import VBox
from utils.colors import WHITE
from utils.navigation import *
from viz.circuit_diagram import CircuitDiagram
from viz.measurements_histogram import MeasurementsHistogram
from viz.qsphere import QSphere
from viz.statevector_grid import StatevectorGrid
from viz.unitary_grid import UnitaryGrid
from controls.circuit_grid import *

WINDOW_SIZE = 1500, 1000

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


def main():
    pygame.display.set_caption('Quantum Circuit Game')

    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare objects
    clock = pygame.time.Clock()

    circuit_grid_model = CircuitGridModel(3, 13)

    circuit_grid_model.set_node(0, 0, node_types.X, np.pi/8)
    circuit_grid_model.set_node(1, 0, node_types.Y, np.pi/6)
    circuit_grid_model.set_node(2, 0, node_types.Z, np.pi/4)

    circuit_grid_model.set_node(0, 1, node_types.X)
    circuit_grid_model.set_node(1, 1, node_types.Y)
    circuit_grid_model.set_node(2, 1, node_types.Z)

    circuit_grid_model.set_node(0, 2, node_types.S)
    circuit_grid_model.set_node(1, 2, node_types.T)
    circuit_grid_model.set_node(2, 2, node_types.H)

    circuit_grid_model.set_node(0, 3, node_types.SDG)
    circuit_grid_model.set_node(1, 3, node_types.TDG)
    circuit_grid_model.set_node(2, 3, node_types.IDEN)

    circuit_grid_model.set_node(0, 4, node_types.X, 0, 2)
    circuit_grid_model.set_node(1, 4, node_types.TRACE)

    circuit_grid_model.set_node(0, 5, node_types.IDEN)
    circuit_grid_model.set_node(2, 5, node_types.Z, np.pi/4, 1)

    circuit_grid_model.set_node(2, 6, node_types.X, 0, 0, 1)

    circuit_grid_model.set_node(1, 7, node_types.H, 0, 2)
    circuit_grid_model.set_node(0, 7, node_types.IDEN)

    circuit_grid_model.set_node(1, 8, node_types.Y, 0, 0)
    circuit_grid_model.set_node(2, 8, node_types.IDEN)

    circuit_grid_model.set_node(2, 9, node_types.Z, 0, 0)

    circuit_grid_model.set_node(0, 10, node_types.IDEN)
    circuit_grid_model.set_node(1, 10, node_types.SWAP, 0, -1, -1, 2)

    circuit_grid_model.set_node(2, 11, node_types.SWAP, 0, 1, -1, 0)

    print("str(circuit_grid_model): ", str(circuit_grid_model))
    circuit = circuit_grid_model.compute_circuit()


    circuit_diagram = CircuitDiagram(circuit)
    unitary_grid = UnitaryGrid(circuit)
    histogram = MeasurementsHistogram(circuit)
    qsphere = QSphere(circuit)
    statevector_grid = StatevectorGrid(circuit)

    left_sprites = VBox(0, 0, circuit_diagram, qsphere)
    middle_sprites = VBox(600, 200, histogram, unitary_grid)
    right_sprites = VBox(1300, 0, statevector_grid)

    circuit_grid = CircuitGrid(10, 700, circuit_grid_model)
    screen.blit(background, (0, 0))

    # pygame.display.flip()



    # screen.blit(background, (0, 0))
    left_sprites.draw(screen)
    middle_sprites.draw(screen)
    right_sprites.draw(screen)
    circuit_grid.draw(screen)
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
            # print("event: ", event)
            if event.type == QUIT:
                going = False

            elif event.type == KEYDOWN:
                index_increment = 0
                if event.key == K_ESCAPE:
                    going = False
                elif event.key == K_LEFT:
                    circuit_grid.move_to_adjacent_node(MOVE_LEFT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_RIGHT:
                    circuit_grid.move_to_adjacent_node(MOVE_RIGHT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_UP:
                    circuit_grid.move_to_adjacent_node(MOVE_UP)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_DOWN:
                    circuit_grid.move_to_adjacent_node(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == K_x:
                    circuit_grid.handle_input_x()
                elif event.key == K_d:
                    circuit_grid.handle_input_delete()
                elif event.key == K_SPACE:
                    screen.blit(background, (0, 0))
                    circuit = circuit_grid_model.compute_circuit()

                    circuit_diagram.set_circuit(circuit)
                    unitary_grid.set_circuit(circuit)
                    qsphere.set_circuit(circuit)
                    histogram.set_circuit(circuit)
                    statevector_grid.set_circuit(circuit)

                    left_sprites.arrange()
                    middle_sprites.arrange()
                    right_sprites.arrange()

                    left_sprites.draw(screen)
                    middle_sprites.draw(screen)
                    right_sprites.draw(screen)

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
