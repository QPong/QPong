import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import circuit_node_types as node_types

class CircuitGridModel():
    """Grid-based model that is built when user interacts with circuit"""
    def __init__(self, max_wires, max_columns):
        self.max_wires = max_wires
        self.max_columns = max_columns
        self.nodes = np.empty((max_wires, max_columns),
                                dtype = CircuitGridNode)

    def set_node(self, wire_num, column_num, node_type, radians=0):
        if not self.nodes[wire_num][column_num]:
            self.nodes[wire_num][column_num] = CircuitGridNode(node_type, radians)
        else:
            print('Node ', wire_num, column_num, ' not empty')

    def get_node(self, wire_num, column_num):
        return self.nodes[wire_num][column_num]

    def compute_circuit(self):
        qr = QuantumRegister(self.max_wires, 'q')
        qc = QuantumCircuit(qr)

        for column_num in range(self.max_columns):
            for wire_num in range(self.max_wires):
                node = self.nodes[wire_num][column_num]
                if node:
                    if node.node_type == node_types.X:
                        qc.x(qr[wire_num])
                    elif node.node_type == node_types.Y:
                        qc.y(qr[wire_num])
                    elif node.node_type == node_types.Z:
                        qc.z(qr[wire_num])
                    elif node.node_type == node_types.H:
                        qc.h(qr[wire_num])
                    elif node.node_type == node_types.B:
                        qc.barrier(qr[wire_num])

        return qc



class CircuitGridNode():
    """Represents a node in the circuit grid"""
    def __init__(self, node_type, radians):
        self.node_type = node_type
        self.radians = radians

    def __str__(self):
        string = 'node_type: ' + str(self.node_type)
        return string
