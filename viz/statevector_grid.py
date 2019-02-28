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
from utils.fonts import ARIAL_30
from utils.states import comp_basis_states
#from utils.paddle import *

class StatevectorGrid(pygame.sprite.Sprite):
    """Displays a statevector grid"""
    def __init__(self, circuit, qubit_num):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.basis_states = comp_basis_states(circuit.width())
        self.set_circuit(circuit, qubit_num)


    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit, qubit_num, shot_num):
        backend_sv_sim = BasicAer.get_backend('statevector_simulator')
        job_sim = execute(circuit, backend_sv_sim, shot_num)
        result_sim = job_sim.result()

        quantum_state = result_sim.get_statevector(circuit, decimals=3)

        # This square represent the probability of state after measurement
        self.image = pygame.Surface([(circuit.width()+1) * 50, 500])
        self.image.convert()
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        block_size = int(round(500 / 2 ** qubit_num))
        x_offset = 50
        y_offset = 15


        self.paddle = pygame.Surface([10, block_size])
        self.paddle.convert()


        for y in range(len(quantum_state)):
            text_surface = ARIAL_30.render(self.basis_states[y], False, (0, 0, 0))
            self.image.blit(text_surface,(120, y * block_size + y_offset))
            if abs(quantum_state[y]) > 0:
                #pygame.draw.rect(self.image, WHITE, rect, 0)
                self.paddle.fill(WHITE)
                self.paddle.set_alpha(int(round(abs(quantum_state[y])*255)))
                self.image.blit(self.paddle,(80,y * block_size))

