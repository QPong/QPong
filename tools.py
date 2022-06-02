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
import os

import pygame as pg
from pygame.constants import RLEACCEL

from prepare import WIDTH_UNIT

MAX_NUM_QUBITS = 10

data_dir = "data"


def load_image(name, colorkey=None, scale=WIDTH_UNIT / 13):
    fullname = os.path.join(data_dir, "images", name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        # raise SystemExit(str(geterror()))
        raise SystemExit()
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    image = pg.transform.scale(
        image, tuple(round(scale * x) for x in image.get_rect().size)
    )
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, "sound", name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error:
        print("Cannot load sound: %s" % fullname)
        # raise SystemExit(str(geterror()))
        raise SystemExit()
    return sound


def comp_basis_states(num_qubits):
    num_qb = min(num_qubits, MAX_NUM_QUBITS)
    basis_states = []
    for idx in range(2**num_qb):
        state = format(idx, "0" + str(num_qb) + "b")
        basis_states.append(state)
    return basis_states
