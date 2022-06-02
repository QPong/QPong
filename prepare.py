import os

import pygame as pg

pg.init()

# Sound effects paths
_BOUNCE_SOUND_PATH = os.path.join(
    "data", "sounds", "4391__noisecollector__pongblipf-5.wav"
)
_EDGE_SOUND_PATH = os.path.join(
    "data", "sounds", "4390__noisecollector__pongblipf-4.wav"
)
_LOST_SOUND_PATH = os.path.join(
    "data", "sounds", "4384__noisecollector__pongblipd4.wav"
)

# Sound effects
SOUND_EFFECTS = {
    "BOUNCE": pg.mixer.Sound(_BOUNCE_SOUND_PATH),
    "EDGE": pg.mixer.Sound(_EDGE_SOUND_PATH),
    "LOST": pg.mixer.Sound(_LOST_SOUND_PATH),
}

# For lower resolution screen
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WIDTH_UNIT = round(WINDOW_WIDTH / 100)

# Font paths
_FONT_PATH = os.path.join("data", "fonts", "bit5x3.ttf")

# Fonts
FONTS = {
    "GAMEOVER": pg.font.Font(_FONT_PATH, 10 * WIDTH_UNIT),
    "CREDIT": pg.font.Font(_FONT_PATH, 2 * WIDTH_UNIT),
    "REPLAY": pg.font.Font(_FONT_PATH, 5 * WIDTH_UNIT),
    "SCORE": pg.font.Font(_FONT_PATH, 12 * WIDTH_UNIT),
    "VECTOR": pg.font.Font(_FONT_PATH, 3 * WIDTH_UNIT),
    "PLAYER": pg.font.Font(_FONT_PATH, 3 * WIDTH_UNIT),
}

# Colors
COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "CYAN": (0, 255, 255),
    "MAGENTA": (255, 0, 255),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "YELLOW": (255, 255, 0),
    "GRAY": (128, 128, 128),
}

QUBIT_NUM = 3
CIRCUIT_DEPTH = 18
WIN_SCORE = 7

# Moves
MOVES = {
    "LEFT": 1,
    "RIGHT": 2,
    "UP": 3,
    "DOWN": 4,
    "X": 5,
    "Y": 6,
    "Z": 7,
    "H": 8,
    "DELETE_GATE": 9,
    "CONTROL_GATE": 10,
}

# Modes
MODES = {
    "ONE_PLAYER": 1,
    "TWO_PLAYER": 2,
}

# Player poistion
POSITIONS = {"LEFT": 0, "RIGHT": 1}

# Ball actions
BALL_ACTIONS = {"NOTHING": 0, "MEASURE_RIGHT": 1, "MEASURE_LEFT": 2}

# Types of players
CLASSICAL_COMPUTER = 0
QUANTUM_COMPUTER_1P = 1
QUANTUM_COMPUTER_2P = 2

KEY_BINDINGS_1P = {
    pg.K_a: MOVES["LEFT"],
    pg.K_d: MOVES["RIGHT"],
    pg.K_w: MOVES["UP"],
    pg.K_s: MOVES["DOWN"],
    pg.K_r: MOVES["X"],
    pg.K_t: MOVES["Y"],
    pg.K_y: MOVES["Z"],
    pg.K_u: MOVES["H"],
    pg.K_i: MOVES["DELETE_GATE"],
    pg.K_o: MOVES["CONTROL_GATE"],
}

KEY_BINDINGS_2P = {
    pg.K_LEFT: MOVES["LEFT"],
    pg.K_RIGHT: MOVES["RIGHT"],
    pg.K_UP: MOVES["UP"],
    pg.K_DOWN: MOVES["DOWN"],
    pg.K_v: MOVES["X"],
    pg.K_b: MOVES["Y"],
    pg.K_n: MOVES["Z"],
    pg.K_m: MOVES["H"],
    pg.K_COMMA: MOVES["DELETE_GATE"],
    pg.K_PERIOD: MOVES["CONTROL_GATE"],
}

# Gamepad
GAMEPAD = {
    "BTN_X": 0,  # PS4 gamepad is 3, PS3 gamepad is 2
    "BTN_Y": 3,
    "BTN_A": 1,  # PS4 gamepad is 1, PS3 gamepad is 3
    "BTN_B": 2,
    "BTN_LEFT_BUMPER": 4,
    "BTN_RIGHT_BUMPER": 5,
    "BTN_LEFT_TRIGGER": 6,
    "BTN_RIGHT_TRIGGER": 7,
    "BTN_SELECT": 8,
    "BTN_START": 9,
    "BTN_LEFT_THUMB": 10,
    "BTN_RIGHT_THUMB": 11,
    "BTN_HOME": 12,  # Not present on PS3
    "BTN_TOUCHPAD": 13,  # Not present on PS3
    "AXIS_LEFT_THUMB_X": 0,
    "AXIS_LEFT_THUMB_Y": 1,
    "AXIS_RIGHT_THUMB_X": 2,
    "AXIS_RIGHT_THUMB_Y": 3,
    "AXIS_LEFT_TRIGGER": 4,  # Not present on PS3
    "AXIS_RIGHT_TRIGGER": 5,
}
