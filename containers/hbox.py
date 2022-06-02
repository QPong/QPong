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
import pygame as pg


class HBox(pg.sprite.RenderPlain):
    """Arranges sprites horizontally"""

    def __init__(self, x, y, *sprites):
        pg.sprite.RenderPlain.__init__(self, sprites)
        self._x = x
        self._y = y
        self.arrange()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def arrange(self):
        next_xpos = self._x
        next_ypos = self._y
        sprite_list = self.sprites()
        for sprite in sprite_list:
            sprite.rect.left = next_xpos
            sprite.rect.top = next_ypos
            next_xpos += sprite.rect.width
