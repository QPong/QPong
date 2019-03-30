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

from pygame.locals import *

from model.circuit_grid_model import *
from containers.vbox import VBox
from utils.gamepad import *
from viz.circuit_diagram import CircuitDiagram
from viz.statevector_grid import StatevectorGrid
from viz.statevector_grid_1 import StatevectorGrid1
from viz.unitary_grid import UnitaryGrid
from controls.circuit_grid import *

from utils.ball import *
from utils.removeball import *
from utils.measurement import *
from utils.collapse_paddle import *
from utils.score import *
import random

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
background.fill(BLACK)

pygame.font.init()

QUBIT_NUM=3
CIRCUIT_DEPTH=18

def update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites, circuit_grid, statevector_grid):
    # Update visualizations
    # TODO: Refactor following code into methods, etc.
    circuit = circuit_grid_model.compute_circuit()
    statevector_grid.set_circuit(circuit, QUBIT_NUM, 100)
    right_sprites.arrange()
    #left_sprite_computer.arrange()
    #right_sprites.draw(screen)
    #left_sprite_computer.draw(screen)
    circuit_grid.draw(screen)
    pygame.display.flip()

def main():
    pygame.display.set_caption('QPong')

    screen.fill(BLACK)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare objects
    clock = pygame.time.Clock()
    oldclock = pygame.time.get_ticks()
    newclock = pygame.time.get_ticks()

    circuit_grid_model = CircuitGridModel(QUBIT_NUM, CIRCUIT_DEPTH)

    # the game crashes if the circuit is empty
    # initialize circuit with 3 identity gate at the end to prevent crash
    # identitiy gate are displayed by completely transparent PNG
    circuit_grid_model.set_node(0, CIRCUIT_DEPTH-1, CircuitGridNode(node_types.IDEN))
    circuit_grid_model.set_node(1, CIRCUIT_DEPTH-1, CircuitGridNode(node_types.IDEN))
    circuit_grid_model.set_node(2, CIRCUIT_DEPTH-1, CircuitGridNode(node_types.IDEN))

    circuit = circuit_grid_model.compute_circuit()


    circuit_diagram = CircuitDiagram(circuit)
    unitary_grid = UnitaryGrid(circuit)
    statevector_grid = StatevectorGrid(circuit, QUBIT_NUM, 100)
    statevector_grid_1 = StatevectorGrid1(circuit)

    score=Score()

    right_sprites = VBox(WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0, statevector_grid)
    left_sprite_computer = VBox(0,0, statevector_grid_1)

    circuit_grid = CircuitGrid(20, WINDOW_HEIGHT*0.51, circuit_grid_model)
    screen.blit(background, (0, 0))

    # computer paddle
    left_box = pygame.sprite.Sprite()
    left_box.image = pygame.Surface([10, 150])
    left_box.image.fill((255, 255, 255))
    left_box.image.set_alpha(255)

    left_box.rect = left_box.image.get_rect()
    left_box.rect.x = 80

    # player paddle
    right_box = pygame.sprite.Sprite()
    right_box.image = pygame.Surface([15, int(round(500 / 2 ** QUBIT_NUM))])
    right_box.image.fill((255, 0, 255))
    right_box.image.set_alpha(0)

    ball = Ball()
    movingsprites = pygame.sprite.Group()
    movingsprites.add(ball)

    ball.ball_reset()
    pygame.display.flip()

    gamepad_repeat_delay = 100
    gamepad_neutral = True
    gamepad_pressed_timer = 0
    gamepad_last_update = pygame.time.get_ticks()

    measure_time = 100000

    # Main Loop
    going = True
    while going:
        # set maximum framerate
        clock.tick(60)
        screen.fill(BLACK)
        ball.update()

        statevector_grid.displaye_statevector(QUBIT_NUM)
        right_sprites.draw(screen)
        # left_sprite_computer.draw(screen)
        movingsprites.draw(screen)
        circuit_grid.draw(screen)

        # Print the score
        scoreprint = "Computer: " + str(score.get_score(0))
        text = ARIAL_30.render(scoreprint, 1, WHITE)
        textpos = (300, 10)
        screen.blit(text, textpos)

        scoreprint = "Player: " + str(score.get_score(1))
        text = ARIAL_30.render(scoreprint, 1, WHITE)
        textpos = (700, 10)
        screen.blit(text, textpos)

        gamepad_move = False

        # computer paddle movement
        if pygame.time.get_ticks() - oldclock > 2000:
            left_box.rect.y = random.randint(0, 400)
            oldclock = pygame.time.get_ticks()

        # update
        lbox = pygame.sprite.Group()
        lbox.add(left_box)
        lbox.draw(screen)

        # use joystick if it's connected
        if num_joysticks > 0:
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
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.button == BTN_X:
                    # Place Y gate
                    circuit_grid.handle_input_y()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.button == BTN_B:
                    # Place Z gate
                    circuit_grid.handle_input_z()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.button == BTN_Y:
                    # Place Hadamard gate
                    circuit_grid.handle_input_h()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.button == BTN_RIGHT_TRIGGER:
                    # Delete gate
                    circuit_grid.handle_input_delete()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.button == BTN_RIGHT_THUMB:
                    # Add or remove a control
                    circuit_grid.handle_input_ctrl()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.button == BTN_LEFT_BUMPER:
                    # Update visualizations
                    # TODO: Refactor following code into methods, etc.
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)

            elif event.type == JOYAXISMOTION:
                # print("event: ", event)
                if event.axis == AXIS_RIGHT_THUMB_X and joystick.get_axis(AXIS_RIGHT_THUMB_X) >= 0.95:
                    circuit_grid.handle_input_rotate(np.pi / 8)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                if event.axis == AXIS_RIGHT_THUMB_X and joystick.get_axis(AXIS_RIGHT_THUMB_X) <= -0.95:
                    circuit_grid.handle_input_rotate(-np.pi / 8)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                if event.axis == AXIS_RIGHT_THUMB_Y and joystick.get_axis(AXIS_RIGHT_THUMB_Y) <= -0.95:
                    circuit_grid.handle_input_move_ctrl(MOVE_UP)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                if event.axis == AXIS_RIGHT_THUMB_Y and joystick.get_axis(AXIS_RIGHT_THUMB_Y) >= 0.95:
                    circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
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
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_y:
                    circuit_grid.handle_input_y()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_z:
                    circuit_grid.handle_input_z()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_h:
                    circuit_grid.handle_input_h()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_SPACE:
                    circuit_grid.handle_input_delete()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_c:
                    # Add or remove a control
                    circuit_grid.handle_input_ctrl()
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_UP:
                    # Move a control qubit up
                    circuit_grid.handle_input_move_ctrl(MOVE_UP)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_DOWN:
                    # Move a control qubit down
                    circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_LEFT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(-np.pi/8)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_RIGHT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(np.pi / 8)
                    circuit_grid.draw(screen)
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)
                    pygame.display.flip()
                elif event.key == K_TAB:
                    # Update visualizations
                    # TODO: Refactor following code into methods, etc.
                    update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                                  circuit_grid, statevector_grid)

        # check ball location and decide what to do
        ball.action()

        if ball.ball_action == MEASURE_RIGHT:
            #
            circuit = circuit_grid_model.compute_circuit()
            circuit_diagram.set_circuit(circuit)
            unitary_grid.set_circuit(circuit)
            pos = statevector_grid.set_circuit_measure(circuit, QUBIT_NUM, 1)
            right_sprites.arrange()
            #left_sprite_computer.arrange()
            #right_sprites.draw(screen)

            balls = pygame.sprite.Group()
            balls.add(ball)

            # paddle after measurement

            right_box.rect = right_box.image.get_rect()
            right_box.rect.x = right_sprites.xpos + 75
            right_box.rect.y = pos * 500/(2**QUBIT_NUM)

            measure_time=pygame.time.get_ticks()

        if ball.ball_action == BOUNCE_RIGHT:
            if pygame.sprite.spritecollide(right_box, balls, False):
                ball.bounce_edge()
                score.update(1)

        if ball.ball_action == BOUNCE_LEFT:
            if pygame.sprite.spritecollide(left_box, balls, False):
                ball.bounce_edge()
                score.update(0)
        if pygame.time.get_ticks()-measure_time > 400:
            #refresh the screen a moment after measurement to update visual
            update_paddle(circuit, circuit_grid_model, left_sprite_computer, right_sprites,
                          circuit_grid, statevector_grid)
            # add a buffer time before measure again
            measure_time = pygame.time.get_ticks() + 100000

        # Update the screen
        pygame.display.flip()

    pygame.quit()


def move_update_circuit_grid_display(circuit_grid, direction):
    circuit_grid.move_to_adjacent_node(direction)
    circuit_grid.draw(screen)
    pygame.display.flip()


if __name__ == '__main__':
    main()
