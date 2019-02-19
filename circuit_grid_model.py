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

    def __str__(self):
        retval = ''
        for wire_num in range(self.max_wires):
            retval += '\n'
            for column_num in range(self.max_columns):
                retval += str(self.nodes[wire_num][column_num]) + ', '

        return 'CircuitGridModel: ' + retval

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
            # First, handle case in which multi-qubit gates are specified
            if not self.compute_multi_qubit_gate(qc, qr, column_num):
                for wire_num in range(self.max_wires):
                    node = self.nodes[wire_num][column_num]
                    if node:
                        if node.node_type == node_types.IDEN:
                            qc.iden(qr[wire_num])
                        elif node.node_type == node_types.X:
                            if node.radians == 0:
                                qc.x(qr[wire_num])
                            else:
                                qc.rx(node.radians, qr[wire_num])
                        elif node.node_type == node_types.Y:
                            if node.radians == 0:
                                qc.y(qr[wire_num])
                            else:
                                qc.ry(node.radians, qr[wire_num])
                        elif node.node_type == node_types.Z:
                            if node.radians == 0:
                                qc.z(qr[wire_num])
                            else:
                                qc.rz(node.radians, qr[wire_num])
                        elif node.node_type == node_types.S:
                            qc.s(qr[wire_num])
                        elif node.node_type == node_types.SDG:
                            qc.sdg(qr[wire_num])
                        elif node.node_type == node_types.T:
                            qc.t(qr[wire_num])
                        elif node.node_type == node_types.TDG:
                            qc.tdg(qr[wire_num])
                        elif node.node_type == node_types.H:
                            qc.h(qr[wire_num])
                        elif node.node_type == node_types.B:
                            qc.barrier(qr)

        return qc

    def compute_multi_qubit_gate(self, qc, qr, column_num):
        print('Column ', column_num, ': ', str(self.nodes[:, column_num]))
        for wire_num in range(self.max_wires):
            node = self.nodes[wire_num][column_num]
            if node:
                if node.node_type == node_types.C:
                    qc.cx(qr[0], qr[1])
                    return True
        return False

class CircuitGridNode():
    """Represents a node in the circuit grid"""
    def __init__(self, node_type, radians):
        self.node_type = node_type
        self.radians = radians

    def __str__(self):
        string = 'type: ' + str(self.node_type)
        string += ', radians: ' + str(self.radians) if self.radians != 0 else ''
        return string
