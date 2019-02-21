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

from utils.colors import *
from utils.fonts import *
from utils.states import comp_basis_states


class UnitaryGrid(pygame.sprite.Sprite):
    """Displays a unitary matrix grid"""
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
        backend_unit_sim = BasicAer.get_backend('unitary_simulator')
        job_sim = execute(circuit, backend_unit_sim)
        result_sim = job_sim.result()

        unitary = result_sim.get_unitary(circuit, decimals=3)
        # print('unitary: ', unitary)

        self.image = pygame.Surface([100 + len(unitary) * 50, 100 + len(unitary) * 50])
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        block_size = 30
        x_offset = 50
        y_offset = 50
        for y in range(len(unitary)):
            text_surface = ARIAL_16.render(self.basis_states[y], False, (0, 0, 0))
            self.image.blit(text_surface,(x_offset, (y + 1) * block_size + y_offset))
            for x in range(len(unitary)):
                text_surface = ARIAL_16.render(self.basis_states[x], False, (0, 0, 0))
                self.image.blit(text_surface, ((x + 1) * block_size + x_offset, y_offset))
                rect = pygame.Rect((x + 1) * block_size + x_offset,
                                   (y + 1) * block_size + y_offset,
                                   abs(unitary[y][x]) * block_size,
                                   abs(unitary[y][x]) * block_size)
                if abs(unitary[y][x]) > 0:
                    pygame.draw.rect(self.image, BLACK, rect, 1)