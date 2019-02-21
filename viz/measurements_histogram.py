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
from qiskit import BasicAer, QuantumRegister, ClassicalRegister, QuantumCircuit, execute
from qiskit.tools.visualization import plot_histogram

from utils import load_image

DEFAULT_NUM_SHOTS = 100

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
        histogram.savefig("utils/data/bell_histogram.png")

        self.image, self.rect = load_image('bell_histogram.png', -1)
        self.image.convert()
