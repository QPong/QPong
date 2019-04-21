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
from viz.statevector_grid import StatevectorGrid
from controls.circuit_grid import *

from utils.ball import *
from utils.score import *
from utils.fonts import *
from utils.parameters import *
from utils.scene import *
from utils.level import *
from utils.input import *

import random

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

pygame.init()

# hardware acceleration to reduce flickering. Works only in fullscreen
flags = DOUBLEBUF|HWSURFACE|FULLSCREEN
screen = pygame.display.set_mode(WINDOW_SIZE, flags)
scene = Scene()
level = Level()
input = Input()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

pygame.font.init()

def main():
    pygame.display.set_caption('QPong')
    screen.fill(BLACK)

    # Prepare objects
    clock = pygame.time.Clock()
    oldclock = pygame.time.get_ticks()

    ball = Ball()
    balls = pygame.sprite.Group()
    balls.add(ball)

    # Show start screen to select difficulty
    input.going = scene.start(screen, ball)
    level.level_setup(scene, ball)
    
    movingsprites = pygame.sprite.Group()
    movingsprites.add(ball)
    movingsprites.add(level.left_box)
    movingsprites.add(level.right_box)

    pygame.display.flip()

    ball.ball_reset()

    measure_time = 100000

    # Main Loop
    while input.going:
        # set maximum frame rate
        clock.tick(60)

        screen.fill(BLACK)

        ball.update()

        for i in range(10, ball.screenheight, 2 * WIDTH_UNIT):  # draw dashed line
            pygame.draw.rect(screen, GRAY, (WINDOW_WIDTH // 2 - 5, i, 0.5 * WIDTH_UNIT, WIDTH_UNIT), 0)

        # Print the score
        text = PLAYER_FONT.render('Classical Computer', 1, GRAY)
        textpos = text.get_rect(center=(round(WINDOW_WIDTH * 0.25) + WIDTH_UNIT * 4.5, WIDTH_UNIT * 1.5))
        screen.blit(text, textpos)

        text = PLAYER_FONT.render('Quantum Computer', 1, GRAY)
        textpos = text.get_rect(center=(round(WINDOW_WIDTH * 0.75) - WIDTH_UNIT * 4.5, WIDTH_UNIT * 1.5))
        screen.blit(text, textpos)

        scoreprint = str(ball.check_score(0))
        text = SCORE_FONT.render(scoreprint, 1, GRAY)
        textpos = text.get_rect(center=(round(WINDOW_WIDTH * 0.25) + WIDTH_UNIT * 4.5, WIDTH_UNIT * 8))
        screen.blit(text, textpos)

        scoreprint = str(ball.check_score(1))
        text = SCORE_FONT.render(scoreprint, 1, GRAY)
        textpos = text.get_rect(center=(round(WINDOW_WIDTH * 0.75) - WIDTH_UNIT * 4.5, WIDTH_UNIT * 8))
        screen.blit(text, textpos)

        level.statevector_grid.display_statevector(scene.qubit_num)
        level.right_sprites.draw(screen)
        movingsprites.draw(screen)
        level.circuit_grid.draw(screen)

        # Show game over screen if the score reaches WIN_SCORE, reset everything if replay == TRUE
        if ball.score.get_score(CLASSICAL_COMPUTER) >= WIN_SCORE:
            scene.gameover(screen, CLASSICAL_COMPUTER)
            scene.replay(screen, ball.score, level.circuit_grid_model, level.circuit_grid)
            input.update_paddle(level, screen, scene)


        if ball.score.get_score(QUANTUM_COMPUTER) >= WIN_SCORE:
            scene.gameover(screen, QUANTUM_COMPUTER)
            scene.replay(screen, ball.score, level.circuit_grid_model, level.circuit_grid)
            input.update_paddle(level, screen, scene)

        # computer paddle movement
        if pygame.time.get_ticks() - oldclock > 300:
            level.left_box.rect.y = ball.get_ypos()- level.statevector_grid.block_size/2+random.randint(-WIDTH_UNIT*4, WIDTH_UNIT*4)
            oldclock = pygame.time.get_ticks()

        # handle input events
        input.handle_input(level, screen, scene)

        # check ball location and decide what to do
        ball.action()

        if ball.ball_action == MEASURE_RIGHT:
            #
            circuit = level.circuit_grid_model.compute_circuit()
            pos = level.statevector_grid.set_circuit_measure(circuit, scene.qubit_num, 1)
            level.right_sprites.arrange()

            # paddle after measurement
            level.right_box.rect.y = pos * ball.screenheight/(2**scene.qubit_num)

            measure_time=pygame.time.get_ticks()

        if pygame.sprite.spritecollide(level.right_box, balls, False):
            ball.bounce_edge()

        if pygame.sprite.spritecollide(level.left_box, balls, False):
            ball.bounce_edge()

        if pygame.time.get_ticks()-measure_time > 400:
            # refresh the screen a moment after measurement to update visual
            input.update_paddle(level, screen, scene)
            # add a buffer time before measure again
            measure_time = pygame.time.get_ticks() + 100000

        # Update the screen
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
