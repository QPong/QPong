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
from utils.parameters import *

def update_paddle(screen, circuit_grid_model, right_sprites, circuit_grid, statevector_grid):
    # Update visualizations
    # TODO: Refactor following code into methods, etc.
    circuit = circuit_grid_model.compute_circuit()
    statevector_grid.set_circuit(circuit, QUBIT_NUM, 100)
    right_sprites.arrange()
    circuit_grid.draw(screen)
    pygame.display.flip()