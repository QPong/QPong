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
Test states utilities
"""

import unittest

from qpong.utils.states import comp_basis_states

class TestUtilsStates(unittest.TestCase):
    """
    Test utility function for generating computational basis states
    """

    def test_comp_basis_states_length(self):
        basis_state = comp_basis_states(3)

        self.assertEqual(len(basis_state), 8)

        basis_state = comp_basis_states(2)

        self.assertEqual(len(basis_state), 4)

        basis_state = comp_basis_states(1)

        self.assertEqual(len(basis_state), 2)

    def test_comp_basis_states(self):
        basis_state = comp_basis_states(3)

        for i, state in enumerate(basis_state):
            self.assertEqual(state, format(i, "03b"))
