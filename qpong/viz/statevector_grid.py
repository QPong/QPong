#
# Copyright 2022 the original author or authors.
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
Statevector grid for quantum player
"""

from copy import deepcopy

import pygame

from qiskit import ClassicalRegister
from qiskit.quantum_info import Statevector

from qpong.utils.colors import WHITE, BLACK
from qpong.utils.parameters import WIDTH_UNIT
from qpong.utils.states import comp_basis_states
from qpong.utils.ball import Ball
from qpong.utils.font import Font


class StatevectorGrid(pygame.sprite.Sprite):
    """
    Displays a statevector grid
    """

    def __init__(self, circuit, qubit_num):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.ball = Ball()
        self.font = Font()
        self.block_size = int(round(self.ball.screenheight / 2**qubit_num))
        self.basis_states = comp_basis_states(circuit.width())
        self.circuit = circuit

        self.paddle = pygame.Surface([WIDTH_UNIT, self.block_size])
        self.paddle.fill(WHITE)
        self.paddle.convert()

        self.paddle_before_measurement(circuit, qubit_num)

    def display_statevector(self, qubit_num):
        """
        Draw computational basis for a statevector of a specified
        number of qubits
        """
        for qb_idx in range(2**qubit_num):
            text = self.font.vector_font.render(
                "|" + self.basis_states[qb_idx] + ">", 1, WHITE
            )
            text_height = text.get_height()
            y_offset = self.block_size * 0.5 - text_height * 0.5
            self.image.blit(text, (2 * WIDTH_UNIT, qb_idx * self.block_size + y_offset))

    def paddle_before_measurement(self, circuit, qubit_num):
        """
        Get statevector from circuit, and set the
        paddle(s) alpha values according to basis
        state(s) probabilitie(s)
        """
        self.update()
        self.display_statevector(qubit_num)
        quantum_state = Statevector(circuit)

        for basis_state, ampl in enumerate(quantum_state):
            self.paddle.set_alpha(int(round(abs(ampl) ** 2 * 255)))
            self.image.blit(self.paddle, (0, basis_state * self.block_size))

    def paddle_after_measurement(self, circuit, qubit_num):
        """
        Measure all qubits on circuit
        """
        self.update()
        self.display_statevector(qubit_num)
        measurement_bitstring = Statevector(circuit).sample_memory(1)[0]
        measurement_int = int(measurement_bitstring, 2)

        self.paddle.set_alpha(255)
        self.image.blit(
            self.paddle, (0, measurement_int * self.block_size)
        )

        return measurement_int

    def update(self):
        """
        Update statevector grid
        """
        self.image = pygame.Surface(
            [(self.circuit.width() + 1) * 3 * WIDTH_UNIT, self.ball.screenheight]
        )
        self.image.convert()
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
