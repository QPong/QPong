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
Global constants
"""
# Define global parameters

# For main.py

# For 15-inch MacBook Pro
# WINDOW_WIDTH=2880
# WINDOW_HEIGHT=1800

# For 13-inch MacBook Pro
# WINDOW_WIDTH=2560
# WINDOW_HEIGHT=1600

# For lower resolution screen
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

WIDTH_UNIT = round(WINDOW_WIDTH / 100)
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
QUBIT_NUM = 2
CIRCUIT_DEPTH = 18

WIN_SCORE = 7

# For ball.py
LEFT = 0
RIGHT = 1

MEASURE_RIGHT = 1
MEASURE_LEFT = 2
NOTHING = 0

YES = 1
NO = 0

# For circuit_grid.py
GRID_WIDTH = WIDTH_UNIT * 4.96
GRID_HEIGHT = GRID_WIDTH

GATE_TILE_WIDTH = GRID_WIDTH * 0.76
GATE_TILE_HEIGHT = GATE_TILE_WIDTH

LINE_WIDTH = round(WIDTH_UNIT * 0.15)

# For scene.py
CLASSICAL_COMPUTER = 0
QUANTUM_COMPUTER = 1

EASY = 0.3
NORMAL = 0.6
EXPERT = 1.5

# EASY = NORMAL = EXPERT = 0.6

# For input.py

MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 3
MOVE_DOWN = 4
