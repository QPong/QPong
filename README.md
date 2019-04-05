# QPong
A quantum version of classic game Pong using qikist and pygame. This is a project for the Qiskit Camp 2019 made by Huang Junye, Jarrod Reilly, Anastasia Jeffery and James Weaver based on James Weaver's quantum-circuit-pygame package: https://github.com/JavaFXpert/quantum-circuit-pygame

## Description
Using the Qiskit and Pygame frameworks, create a Pong game in which a human competes against the computer. Each player's "paddle" is realized by a quantum circuit that results in a state vector in a superposition. When the ball gets close to a player's paddle area, the quantum state is measured, collapsing to a basis state that determines the paddle's location.

## Control

### Keyboard
W, A, S, D: Up, Left, Down, Right to move cursor

SPACE: delete gate

X, Y, Z, H: add Pauli-X, Pauli-Y, Pauli-Z, Hadamard gate

C: add CNOT gate

UP, DOWN: move control qubit up or down

Left, Right: add rotation to a gate, at pi/8 step

TAB: update visulization


### Joystick
Joystick button correspondence depends on the model of joystick. Details will be added later

## Credits
Sound effects are made by NoiseCollector from Freesound.org: https://freesound.org/people/NoiseCollector/packs/254/
Font used in the game is Bit5x3 made by Matt LaGrandeur: http://www.mattlag.com/bitfonts/
