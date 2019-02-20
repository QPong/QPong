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
from qiskit import execute
from qiskit import BasicAer
from qiskit.tools.visualization import plot_histogram

from circuit_grid_model import *
import circuit_node_types as node_types
from containers.vbox import VBox
from utils.colors import WHITE, BLACK
from utils.resources import load_image
from viz.circuit_diagram import CircuitDiagram
from viz.qsphere import QSphere
from viz.statevector_grid import StatevectorGrid

COMP_BASIS_STATES = ['000', '001', '010', '011', '100', '101', '110', '111']

DEFAULT_NUM_SHOTS = 100

WINDOW_SIZE = 1500, 1200

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)

pygame.font.init()
ARIAL_30 = pygame.font.SysFont('Arial', 30)


def create_circuit():
    """Create a qiskit circuit from the circuit grid"""
    qr = QuantumRegister(2, 'q')
    qc = QuantumCircuit(qr)

    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    return qc


class UnitaryGrid(pygame.sprite.Sprite):
    """Displays a unitary matrix grid"""
    def __init__(self, circuit):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.set_circuit(circuit)

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit):
        backend_unit_sim = BasicAer.get_backend('unitary_simulator')
        job_sim = execute(circuit, backend_unit_sim)
        result_sim = job_sim.result()

        unitary = result_sim.get_unitary(circuit, decimals=3)
        # print('unitary: ', unitary)

        self.image = pygame.Surface([len(unitary) * 50, len(unitary) * 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        block_size = 30
        x_offset = 50
        y_offset = 50
        for y in range(len(unitary)):
            text_surface = ARIAL_30.render(COMP_BASIS_STATES[y], False, (0, 0, 0))
            self.image.blit(text_surface,(x_offset, (y + 1) * block_size + y_offset))
            for x in range(len(unitary)):
                text_surface = ARIAL_30.render(COMP_BASIS_STATES[x], False, (0, 0, 0))
                self.image.blit(text_surface, ((x + 1) * block_size + x_offset, y_offset))
                rect = pygame.Rect((x + 1) * block_size + x_offset,
                                   (y + 1) * block_size + y_offset,
                                   abs(unitary[y][x]) * block_size,
                                   abs(unitary[y][x]) * block_size)
                if abs(unitary[y][x]) > 0:
                    pygame.draw.rect(self.image, BLACK, rect, 1)


class MeasurementsHistogram(pygame.sprite.Sprite):
    """Displays a histogram with measurements"""
    def __init__(self, circuit, num_shots=DEFAULT_NUM_SHOTS):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.set_circuit(circuit, num_shots)

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit, num_shots=DEFAULT_NUM_SHOTS):
        backend_sim = BasicAer.get_backend('qasm_simulator')
        qr = QuantumRegister(circuit.width(), 'q')
        cr = ClassicalRegister(circuit.width(), 'c')
        meas_circ = QuantumCircuit(qr, cr)
        meas_circ.barrier(qr)
        meas_circ.measure(qr, cr)
        complete_circuit = circuit + meas_circ

        job_sim = execute(complete_circuit, backend_sim, shots=num_shots)

        result_sim = job_sim.result()

        counts = result_sim.get_counts(complete_circuit)
        print(counts)

        histogram = plot_histogram(counts)
        histogram.savefig("data/bell_histogram.png")

        self.image, self.rect = load_image('bell_histogram.png', -1)


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

    circuit_grid_model.set_node(0, 4, node_types.X, 0, 1)

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
    # circuit = create_circuit()

    circuit_diagram = CircuitDiagram(circuit)
    unitary_grid = UnitaryGrid(circuit)
    histogram = MeasurementsHistogram(circuit)
    qsphere = QSphere(circuit)
    statevector_grid = StatevectorGrid(circuit)

    left_sprites = VBox(0, 0, circuit_diagram, qsphere)
    # middle_sprites = VBox(600, 0, unitary_grid, histogram)
    middle_sprites = VBox(600, 200, histogram)
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
                    # circuit = create_circuit()

                    circuit_diagram.set_circuit(circuit)
                    unitary_grid.set_circuit(circuit)
                    qsphere.set_circuit(circuit)
                    histogram.set_circuit(circuit)
                    statevector_grid.set_circuit(circuit)

                    left_sprites.arrange()
                    middle_sprites.arrange()
                    right_sprites.arrange()

        #Draw Everything
        screen.blit(background, (0, 0))

        left_sprites.draw(screen)
        middle_sprites.draw(screen)
        right_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()