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
"""Create quantum circuits with Qiskit and Pygame"""

import pygame
from pygame.locals import *

from model.circuit_grid_model import *
from model import circuit_node_types as node_types
from containers.vbox import VBox
from utils.colors import WHITE
from viz.circuit_diagram import CircuitDiagram
from viz.measurements_histogram import MeasurementsHistogram
from viz.qsphere import QSphere
from viz.statevector_grid import StatevectorGrid
from viz.unitary_grid import UnitaryGrid

WINDOW_SIZE = 1500, 1200

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

pygame.init()
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

    # circuit_grid_model.set_node(0, 5, node_types.Z, np.pi/8)
    circuit_grid_model.set_node(2, 5, node_types.Z, np.pi/4, 1)

    circuit_grid_model.set_node(2, 6, node_types.X, 0, 0, 1)

    circuit_grid_model.set_node(0, 7, node_types.B)

    circuit_grid_model.set_node(1, 8, node_types.H, 0, 2)

    circuit_grid_model.set_node(1, 9, node_types.Y, 0, 0)

    circuit_grid_model.set_node(2, 10, node_types.Z, 0, 0)

    circuit_grid_model.set_node(1, 11, node_types.SWAP, 0, -1, -1, 2)

    circuit_grid_model.set_node(2, 12, node_types.SWAP, 0, 1, -1, 0)

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


    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN:
                index_increment = 0
                if event.key == K_ESCAPE:
                    going = False
                elif event.key == K_RIGHT or event.key == K_DOWN:
                    index_increment = 1
                elif event.key == K_LEFT or event.key == K_UP:
                    index_increment = -1
                if index_increment != 0:
                    circuit = circuit_grid_model.compute_circuit()

                    circuit_diagram.set_circuit(circuit)
                    unitary_grid.set_circuit(circuit)
                    qsphere.set_circuit(circuit)
                    histogram.set_circuit(circuit)
                    statevector_grid.set_circuit(circuit)

                    left_sprites.arrange()
                    middle_sprites.arrange()
                    right_sprites.arrange()

        screen.blit(background, (0, 0))

        left_sprites.draw(screen)
        middle_sprites.draw(screen)
        right_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
