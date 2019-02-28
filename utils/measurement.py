#How to measure the state and output a position?
#Ideas:

# 1. Get the state from circuit
# 2. Do one shot measurement using qiskit
# 3. Output a position (0~2^n-1)
# 4. Pass to ball class

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
from qiskit import *
from utils.colors import WHITE, BLACK
from utils.fonts import ARIAL_30
from utils.states import comp_basis_states

DEFAULT_NUM_SHOTS = 1
class Measurement():
    """Measure the state"""

    def __init__(self, circuit):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.basis_states = comp_basis_states(circuit.width())
        self.set_circuit(circuit)

    # set up the circuit and do measurement
    def get_position(self, circuit, num_shots=DEFAULT_NUM_SHOTS):
        backend_sim = BasicAer.get_backend('qasm_simulator')
        qr = QuantumRegister(circuit.width(), 'q')
        cr = ClassicalRegister(circuit.width(), 'c')
        meas_circ = QuantumCircuit(qr, cr)
        meas_circ.barrier(qr)
        meas_circ.measure(qr, cr)
        complete_circuit = circuit + meas_circ

        job_sim = execute(complete_circuit, backend_sim, shots=num_shots)

        result_sim = job_sim.result()
        counts = result_sim.get_counts(qc)
        result = list(counts.keys())
        # convert measurement result to a position number
        position = int(result[0], 2)
        return position

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
