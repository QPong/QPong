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
Constants and utilities for quantum states
"""

MAX_NUM_QUBITS = 10


def comp_basis_states(num_qubits):
    """
    Get computational basis states for a quantum state with
    a specified number of qubits
    """
    num_qb = min(num_qubits, MAX_NUM_QUBITS)
    basis_states = []
    for idx in range(2**num_qb):
        state = format(idx, "0" + str(num_qb) + "b")
        basis_states.append(state)
    return basis_states
