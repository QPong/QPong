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

"""
Test circuit grid model
"""

import unittest

from qpong.model import CircuitGridModel, CircuitGridNode
from qpong.model import circuit_node_types as node_types


class TestCircuitGridModel(unittest.TestCase):
    """
    Test utility function for generating computational basis states
    """

    def test_circuit_node_initialization(self):
        """
        Test circuit node initialization
        """
        node = CircuitGridNode(node_types.X)

        self.assertEqual(node.node_type, node_types.X)
        self.assertEqual(node.radians, 0.0)
        self.assertEqual(node.swap, -1.0)
        self.assertEqual(node.ctrl_a, -1.0)
        self.assertEqual(node.ctrl_b, -1.0)

    def test_circuit_grid_model_initialization(self):
        """
        Test circuit grid model initialization
        """
        model = CircuitGridModel(3, 3)

        for wire_num in range(model.max_wires):
            for column_num in range(model.max_columns):
                self.assertEqual(
                    model.get_node(wire_num, column_num).node_type, node_types.EMPTY
                )

    def test_get_node(self):
        """
        Test get node
        """
        model = CircuitGridModel(3, 3)
        node = CircuitGridNode(node_types.X)
        model.set_node(0, 0, node)

        self.assertEqual(model.get_node(0, 0).node_type, node.node_type)
        self.assertEqual(model.get_node(0, 0).radians, node.radians)
        self.assertEqual(model.get_node(0, 0).swap, node.swap)
        self.assertEqual(model.get_node(0, 0).ctrl_a, node.ctrl_a)
        self.assertEqual(model.get_node(0, 0).ctrl_b, node.ctrl_b)

    def test_reset_circuit(self):
        """
        Test reset circuit
        """
        model = CircuitGridModel(3, 3)
        node1 = CircuitGridNode(node_types.Y)
        node2 = CircuitGridNode(node_types.X)
        node3 = CircuitGridNode(node_types.Z)

        model.set_node(0, 0, node1)
        model.set_node(1, 0, node2)
        model.set_node(2, 0, node3)

        model.reset_circuit()

        for wire_num in range(model.max_wires):
            for column_num in range(model.max_columns):
                self.assertEqual(
                    model.get_node(wire_num, column_num).node_type, node_types.EMPTY
                )
