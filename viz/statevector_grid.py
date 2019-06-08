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
import pygame
from qiskit import BasicAer, execute, ClassicalRegister
from utils.colors import WHITE, BLACK
from utils.fonts import VECTOR_FONT
from utils.parameters import WIDTH_UNIT
from utils.states import comp_basis_states
from copy import deepcopy
from utils.ball import Ball


class StatevectorGrid(pygame.sprite.Sprite):
    """Displays a statevector grid"""
    def __init__(self, circuit, qubit_num, num_shots):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.ball = Ball()
        self.block_size = int(round(self.ball.screenheight / 2 ** qubit_num))
        self.basis_states = comp_basis_states(circuit.width())
        self.circuit = circuit

        self.paddle = pygame.Surface([WIDTH_UNIT, self.block_size])
        self.paddle.fill(WHITE)
        self.paddle.convert()

        self.paddle_before_measurement(circuit, qubit_num, num_shots)

    def display_statevector(self, qubit_num):
        for y in range(2**qubit_num):
            text = VECTOR_FONT.render("|"+self.basis_states[y]+">", 1, WHITE)
            text_height = text.get_height()
            y_offset = self.block_size * 0.5 - text_height * 0.5
            self.image.blit(text, (2 * WIDTH_UNIT, y * self.block_size + y_offset))

    def paddle_before_measurement(self, circuit, qubit_num, shot_num):
        self.update()
        self.display_statevector(qubit_num)

        backend_sv_sim = BasicAer.get_backend('statevector_simulator')
        job_sim = execute(circuit, backend_sv_sim, shots=shot_num)
        result_sim = job_sim.result()
        quantum_state = result_sim.get_statevector(circuit, decimals=3)

        for y in range(len(quantum_state)):
            if abs(quantum_state[y]) > 0:
                self.paddle.set_alpha(int(round(abs(quantum_state[y])*255)))
                self.image.blit(self.paddle, (0, y * self.block_size))

    def paddle_after_measurement(self, circuit, qubit_num, shot_num):
        self.update()
        self.display_statevector(qubit_num)

        backend_sv_sim = BasicAer.get_backend('qasm_simulator')
        cr = ClassicalRegister(qubit_num)
        measure_circuit = deepcopy(circuit)  # make a copy of circuit
        measure_circuit.add_register(cr)    # add classical registers for measurement readout
        measure_circuit.measure(measure_circuit.qregs[0], measure_circuit.cregs[0])
        job_sim = execute(measure_circuit, backend_sv_sim, shots=shot_num)
        result_sim = job_sim.result()
        counts = result_sim.get_counts(circuit)

        self.paddle.set_alpha(255)
        self.image.blit(self.paddle, (0, int(list(counts.keys())[0], 2) * self.block_size))

        return int(list(counts.keys())[0], 2)

    def update(self):
        self.image = pygame.Surface([(self.circuit.width() + 1) * 3 * WIDTH_UNIT, self.ball.screenheight])
        self.image.convert()
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
