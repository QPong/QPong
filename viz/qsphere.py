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
from qiskit.tools.visualization import plot_state_qsphere

from utils import load_image


class QSphere(pygame.sprite.Sprite):
    """Displays a qsphere"""
    def __init__(self, circuit):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.set_circuit(circuit)

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit):
        backend_sv_sim = BasicAer.get_backend('statevector_simulator')
        job_sim = execute(circuit, backend_sv_sim)
        result_sim = job_sim.result()

        quantum_state = result_sim.get_statevector(circuit, decimals=3)
        qsphere = plot_state_qsphere(quantum_state)
        qsphere.savefig("utils/data/bell_qsphere.png")

        self.image, self.rect = load_image('bell_qsphere.png', -1)
        self.rect.inflate_ip(-100, -100)
        self.image.convert()
