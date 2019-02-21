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
from qiskit import BasicAer, execute
from utils.colors import WHITE, BLACK
from utils.fonts import ARIAL_30
from utils.states import comp_basis_states


class StatevectorGrid(pygame.sprite.Sprite):
    """Displays a statevector grid"""
    def __init__(self, circuit):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.basis_states = comp_basis_states(circuit.width())
        self.set_circuit(circuit)

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit):
        backend_sv_sim = BasicAer.get_backend('statevector_simulator')
        job_sim = execute(circuit, backend_sv_sim)
        result_sim = job_sim.result()

        quantum_state = result_sim.get_statevector(circuit, decimals=3)

        self.image = pygame.Surface([(circuit.width() + 1) * 50, 100 + len(quantum_state) * 50])
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        block_size = 50
        x_offset = 50
        y_offset = 50
        for y in range(len(quantum_state)):
            text_surface = ARIAL_30.render(self.basis_states[y], False, (0, 0, 0))
            self.image.blit(text_surface,(x_offset, (y + 1) * block_size + y_offset))
            rect = pygame.Rect(x_offset + circuit.width() * 20,
                               (y + 1) * block_size + y_offset,
                               abs(quantum_state[y]) * block_size,
                               abs(quantum_state[y]) * block_size)
            if abs(quantum_state[y]) > 0:
                pygame.draw.rect(self.image, BLACK, rect, 1)
