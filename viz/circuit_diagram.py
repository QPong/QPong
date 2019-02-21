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

from utils.resources import load_image


class CircuitDiagram(pygame.sprite.Sprite):
    """Displays a circuit diagram"""
    def __init__(self, circuit):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.set_circuit(circuit)

    # def update(self):
    #     # Nothing yet
    #     a = 1

    def set_circuit(self, circuit):
        circuit_drawing = circuit.draw(output='mpl')

        # TODO: Create a save_fig method that works cross-platform
        #       and has exception handling
        circuit_drawing.savefig("utils/data/bell_circuit.png")

        self.image, self.rect = load_image('bell_circuit.png', -1)
        self.image.convert()
