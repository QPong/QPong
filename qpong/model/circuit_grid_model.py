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

"""
Grid-based model underlying the circuit grid for the quantum player
"""

import numpy as np

from qiskit import QuantumCircuit, QuantumRegister

from qpong.model import circuit_node_types as node_types


NODE_IDENTIFIERS = {
    0: 'i',
    1: 'x',
    2: 'y',
    3: 'z',
    4: 's',
    5: 'sdg',
    6: 't',
    7: 'tdg',
    8: 'h',
    9: 'swap',
    10: 'c',
}

# pylint: disable=too-few-public-methods
class CircuitGridModel:
    """
    Grid-based model that is built when user interacts with circuit
    """

    def __init__(self, max_wires, max_columns):
        self.max_wires = max_wires
        self.max_columns = max_columns
        self.nodes = np.full((max_wires, max_columns),
                CircuitGridNode(node_types.EMPTY), dtype=CircuitGridNode)

    def __str__(self):
        retval = ""
        for wire_num in range(self.max_wires):
            retval += "\n"
            for column_num in range(self.max_columns):
                retval += str(self.get_node_gate_part(wire_num, column_num)) + ", "
        return "CircuitGridModel: " + retval

    def set_node(self, wire_num, column_num, circuit_grid_node):
        """
        Assign node to a specified wire and column number

        Parameters:
        wire_num (integer): wire number
        column_num (integer): column number
        circuit_grid_node (CircuitGridNode): node to be assigned
        """
        self.nodes[wire_num][column_num] = CircuitGridNode(
            circuit_grid_node.node_type,
            circuit_grid_node.radians,
            circuit_grid_node.ctrl_a,
            circuit_grid_node.ctrl_b,
            circuit_grid_node.swap,
        )

    def get_node(self, wire_num, column_num):
        """
        Get node on a specified wire and column
        number

        Parameters:
        wire_num (integer): wire number
        column_num (integer): column number
        """
        return self.nodes[wire_num][column_num]

    def get_node_gate_part(self, wire_num, column_num):
        """
        Get gate underlying node on specified wire
        and column number

        Parameters:
        wire_num (integer): wire number
        column_num (integer): column number
        """
        requested_node = self.nodes[wire_num][column_num]
        if requested_node.node_type != node_types.EMPTY:
            # Node is occupied so return its gate
            return requested_node.node_type

        # Check for control nodes from gates in other nodes in this column
        nodes_in_column = self.nodes[:, column_num]
        for idx in range(self.max_wires):
            if idx != wire_num:
                other_node = nodes_in_column[idx]
                if wire_num in(
                    other_node.ctrl_a,
                    other_node.ctrl_b
                ):
                    return node_types.CTRL
                if other_node.swap == wire_num:
                    return node_types.SWAP

        return node_types.EMPTY

    def get_gate_wire_for_control_node(self, control_wire_num, column_num):
        """
        Get wire for gate that belongs to a control node on the given wire

        Parameters:
        control_wire_num (integer): wire number of control qubit
        column_num (integer): column number
        """
        gate_wire_num = -1
        nodes_in_column = self.nodes[:, column_num]
        for wire_idx in range(self.max_wires):
            if wire_idx != control_wire_num:
                other_node = nodes_in_column[wire_idx]
                if control_wire_num in (
                    other_node.ctrl_a,
                    other_node.ctrl_b
                ):
                    gate_wire_num = wire_idx
                    print(
                        "Found gate: ",
                        self.get_node_gate_part(gate_wire_num, column_num),
                        " on wire: ",
                        gate_wire_num,
                    )
        return gate_wire_num

    def construct_circuit(self):
        """
        Construct quantum circuit with instruction on circuit grid
        """
        register = QuantumRegister(self.max_wires, "q")
        circuit = QuantumCircuit(register)

        for column_num in range(self.max_columns):
            for wire_num in range(self.max_wires):
                print(column_num, wire_num)
                node = self.nodes[wire_num][column_num]
                attr = []
                args = []

                if node.radians != 0:
                    args.append(node.radians)

                if node.ctrl_a != -1:
                    attr.append("c")
                    args.append(register[node.ctrl_a])

                if node.ctrl_b != -1:
                    attr.append("c")
                    args.append(register[node.ctrl_b])

                if node.swap != -1:
                    attr.append("swap")
                    args.append(register[wire_num])
                    args.append(register[node.swap])
                else:
                    if node.radians !=  0:
                        attr.append("r")
                    if node.node_type != node_types.EMPTY:
                        args.append(register[wire_num])
                        attr.append(NODE_IDENTIFIERS[node.node_type])

                attr = ''.join(attr)
                if hasattr(circuit, attr):
                    getattr(circuit, attr)(*args)

        return circuit

    def reset_circuit(self):
        """
        Reset circuit by reinitializing nodes matrix
        """
        self.nodes = np.full((self.max_wires, self.max_columns),
                CircuitGridNode(node_types.EMPTY) , dtype=CircuitGridNode)

        #for i in range(self.max_wires):
        #    self.set_node(i, CIRCUIT_DEPTH - 1, CircuitGridNode(node_types.IDEN))

class CircuitGridNode:
    """
    Represents a node in the circuit grid
    """

    def __init__(self, node_type, radians=0.0, ctrl_a=-1, ctrl_b=-1, swap=-1):
        self.node_type = node_type
        self.radians = radians
        self.ctrl_a = ctrl_a
        self.ctrl_b = ctrl_b
        self.swap = swap

    def __str__(self):
        string = "type: " + str(self.node_type)
        string += ", radians: " + str(self.radians) if self.radians != 0 else ""
        string += ", ctrl_a: " + str(self.ctrl_a) if self.ctrl_a != -1 else ""
        string += ", ctrl_b: " + str(self.ctrl_b) if self.ctrl_b != -1 else ""
        return string
