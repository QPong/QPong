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
    Unit tests for circuit grid model
    """

    def setUp(self):
        """
        Set up
        """

        self.model = CircuitGridModel(3, 3)
        self.node_x = CircuitGridNode(node_types.X)
        self.node_y = CircuitGridNode(node_types.Y)
        self.node_z = CircuitGridNode(node_types.Z)

    def test_circuit_node_initialization(self):
        """
        Test circuit node initialization
        """

        self.assertEqual(self.node_x.node_type, node_types.X)
        self.assertEqual(self.node_x.radians, 0.0)
        self.assertEqual(self.node_x.swap, -1.0)
        self.assertEqual(self.node_x.ctrl_a, -1.0)
        self.assertEqual(self.node_x.ctrl_b, -1.0)

        self.assertEqual(self.node_y.node_type, node_types.Y)
        self.assertEqual(self.node_y.radians, 0.0)
        self.assertEqual(self.node_y.swap, -1.0)
        self.assertEqual(self.node_y.ctrl_a, -1.0)
        self.assertEqual(self.node_y.ctrl_b, -1.0)

        self.assertEqual(self.node_z.node_type, node_types.Z)
        self.assertEqual(self.node_z.radians, 0.0)
        self.assertEqual(self.node_z.swap, -1.0)
        self.assertEqual(self.node_z.ctrl_a, -1.0)
        self.assertEqual(self.node_z.ctrl_b, -1.0)


    def test_circuit_grid_model_initialization(self):
        """
        Test circuit grid model initialization
        """

        for wire_num in range(self.model.max_wires):
            for column_num in range(self.model.max_columns):
                self.assertEqual(
                    self.model.get_node(wire_num, column_num).node_type, node_types.EMPTY
                )

    def test_get_node(self):
        """
        Test get node
        """

        self.model.set_node(0, 0, self.node_x)

        self.assertEqual(self.model.get_node(0, 0).node_type, self.node_x.node_type)
        self.assertEqual(self.model.get_node(0, 0).radians, self.node_x.radians)
        self.assertEqual(self.model.get_node(0, 0).swap, self.node_x.swap)
        self.assertEqual(self.model.get_node(0, 0).ctrl_a, self.node_x.ctrl_a)
        self.assertEqual(self.model.get_node(0, 0).ctrl_b, self.node_x.ctrl_b)

    def test_reset_circuit(self):
        """
        Test reset circuit
        """

        self.model.set_node(0, 0, self.node_x)
        self.model.set_node(1, 0, self.node_y)
        self.model.set_node(2, 0, self.node_z)

        self.model.reset_circuit()

        for wire_num in range(self.model.max_wires):
            for column_num in range(self.model.max_columns):
                self.assertEqual(
                    self.model.get_node(wire_num, column_num).node_type, node_types.EMPTY
                )
