import pygame as pg

from containers.vbox import VBox
from controls.circuit_grid import CircuitGrid, CircuitGridNode
from model import circuit_node_types as node_types
from model.circuit_grid_model import CircuitGridModel
from prepare import (
    MODES,
    POSITIONS,
    CIRCUIT_DEPTH,
    WIDTH_UNIT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    QUANTUM_COMPUTER_1P,
    QUANTUM_COMPUTER_2P,
)
from viz.statevector_grid import StatevectorGrid


class Player(object):
    """A class to present a quantum player."""

    def __init__(self, qubit_num, position, player_type, game_mode):
        self._position = position
        self._player_type = player_type
        self._score = 0
        self._qubit_num = qubit_num
        self._paddle = pg.sprite.Sprite()
        self._circuit = None
        self._circuit_grid_model = None
        self._statevector_grid = None
        self._statevector = None

        self._circuit_depth = (
            CIRCUIT_DEPTH // 2 if game_mode == MODES["TWO_PLAYER"] else CIRCUIT_DEPTH
        )

        self._circuit_grid_model = CircuitGridModel(qubit_num, self._circuit_depth)

        for i in range(qubit_num):
            self._circuit_grid_model.set_node(
                i, self._circuit_depth - 1, CircuitGridNode(node_types.IDEN)
            )

        self._circuit = self._circuit_grid_model.compute_circuit()

        if POSITIONS["LEFT"] == position:
            self._circuit_grid = CircuitGrid(
                1.45 * WIDTH_UNIT,
                round(WINDOW_HEIGHT * 0.7),
                self._circuit_grid_model,
                game_mode,
            )
            self._statevector_grid = StatevectorGrid(
                self._circuit, position, qubit_num, 100
            )
            self._statevector = VBox(0, WIDTH_UNIT * 0, self._statevector_grid)

        else:
            self._circuit_grid = CircuitGrid(
                WINDOW_WIDTH // 2 if game_mode == MODES["TWO_PLAYER"] else 0,
                round(WINDOW_HEIGHT * 0.7),
                self._circuit_grid_model,
                game_mode,
            )
            self._statevector_grid = StatevectorGrid(
                self._circuit, position, qubit_num, 100
            )
            self._statevector = VBox(
                WIDTH_UNIT * 90, WIDTH_UNIT * 0, self._statevector_grid
            )

        # player paddle for detection of collision. It is invisible on the screen
        self._paddle.image = pg.Surface(
            [WIDTH_UNIT, int(round(WINDOW_HEIGHT * 0.7) / 2**qubit_num)]
        )
        self._paddle.image.fill(
            (
                255,
                0
                if self._player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P)
                else 255,
                255,
            )
        )
        #self._paddle.image.set_alpha(
        #    0
        #    if self._player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P)
        #   else 255
        #)
        self._paddle.rect = self._paddle.image.get_rect()

        if self._player_type in (QUANTUM_COMPUTER_1P, QUANTUM_COMPUTER_2P):
            if POSITIONS["LEFT"] == position:
                self._paddle.rect.x = 9.5 * WIDTH_UNIT
                self._statevector.arrange()
            else:
                self._paddle.rect.x = self._statevector.x

        else:
            self._paddle.rect.x = 9 * WIDTH_UNIT

    @property
    def qubit_num(self):
        return self._qubit_num

    @qubit_num.setter
    def qubit_num(self, value):
        self._qubit_num = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def player_type(self):
        return self._player_type

    @player_type.setter
    def player_type(self, value):
        self._player_type = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def paddle(self):
        return self._paddle

    @paddle.setter
    def paddle(self, value):
        self._paddle = value

    @property
    def circuit(self):
        return self._circuit

    @circuit.setter
    def circuit(self, value):
        self._circuit = value

    @property
    def circuit_grid(self):
        return self._circuit_grid

    @circuit_grid.setter
    def circuit_grid(self, value):
        self._circuit_grid = value

    @property
    def circuit_grid_model(self):
        return self._circuit_grid_model

    @circuit_grid_model.setter
    def circuit_grid_model(self, value):
        self._circuit_grid_model = value

    @property
    def statevector(self):
        return self._statevector

    @statevector.setter
    def statevector(self, value):
        self._statevector = value

    @property
    def statevector_grid(self):
        return self._statevector_grid

    @statevector_grid.setter
    def statevector_grid(self, value):
        self._statevector_grid = value

    def reset_score(self):
        self._score = 0

    def update_paddle(self, screen):
        # Update visualizations
        # TODO: Refactor following code into methods, etc.

        circuit_grid_model = self._circuit_grid_model
        statevector = self._statevector
        circuit_grid = self._circuit_grid
        statevector_grid = self._statevector_grid

        circuit = circuit_grid_model.compute_circuit()
        statevector_grid.paddle_before_measurement(
            self._position, circuit, self._qubit_num, 100
        )
        statevector.arrange()
        circuit_grid.draw(screen)

    def move_update_circuit_grid_display(self, screen, direction):
        self._circuit_grid.move_to_adjacent_node(direction)
        self._circuit_grid.draw(screen)
