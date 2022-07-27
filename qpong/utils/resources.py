#
# Copyright 2022 the original author or authors.
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
Utilities for loading resources (fonts, images and sounds)
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
    if not pygame.get_init():
        pygame.init()

    full_name = os.path.join(data_dir, "images", name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error:
        print("Cannot load image:", full_name)
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
    """
    Load sound with pygame mixer

    Parameters:
    name (string): file name
    """
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    full_name = os.path.join(data_dir, "sound", name)
    try:
        sound = pygame.mixer.Sound(full_name)
    except pygame.error:
        print("Cannot load sound: %s" % full_name)
        error_message = pygame.get_error()
        raise SystemExit(error_message) from pygame.error
    return sound


def load_font(name, size=2 * WIDTH_UNIT):
    """
    Load font with pygame font

    Parameters:
    name (string): file name
    """
    if not pygame.font.get_init():
        pygame.font.init()

    full_name = os.path.join(data_dir, "font", name)
    try:
        font = pygame.font.Font(full_name, size)
    except pygame.error:
        print("Cannot load font: %s" % full_name)
        error_message = pygame.get_error()
        raise SystemExit(error_message) from pygame.error
    return font
