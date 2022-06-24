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
Utilities for loading resources (images and sounds)
"""

import os

import pygame
from qpong.utils.parameters import WIDTH_UNIT

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "..", "data")


def load_image(name, colorkey=None, scale=WIDTH_UNIT / 13):
    """
    Load image with pygame

    Parameters:
    name (string): file name
    """
    fullname = os.path.join(data_dir, "images", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print("Cannot load image:", fullname)
        error_message = pygame.get_error()
        raise SystemExit(error_message) from pygame.error
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    image = pygame.transform.scale(
        image, tuple(round(scale * x) for x in image.get_rect().size)
    )
    return image, image.get_rect()


def load_sound(name):
    # pylint: disable=too-few-public-methods
    """
    Load sound with pygame mixer

    Parameters:
    name (string): file name
    """
    if not pygame.mixer or not pygame.mixer.get_init():
        pygame.mixer.init()

    fullname = os.path.join(data_dir, "sound", name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("Cannot load sound: %s" % fullname)
        error_message = pygame.get_error()
        raise SystemExit(error_message) from pygame.error
    return sound
