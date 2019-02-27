# QPong
A quantum version of classic game Pong using qikist and pygame. This is a project for the Qiskit Camp 2019

## Description
Using the Qiskit and Pygame frameworks, create a Pong game in which a human competes against the computer. Each player's "paddle" is realized by a quantum circuit that results in a state vector in a superposition. When the ball gets close to a player's paddle area, the quantum state is measured, collapsing to a basis state that determines the paddle's location.

## First iteration
The circuit for the computer player's paddle contains two wires, each with one Hadamard gate. No changes are made to the computer player's circuit during gameplay, resulting in a 1/2 probability of the paddle returning the ball. The circuit for the human player's paddle contains three wires, each with one Identity gate. During gameplay, the human player adds and removes Pauli-X gates to the wires in such a way that the paddle's state collapses in a location that returns the ball.

## Second iteration
The circuits for both player's paddles contains four wires, with an Identity gate on each wire. During gameplay, each player adds and removes Pauli-X gates to the wires in such a way that the paddle collapses in a location that returns the ball. In fairness to the human player, the computer may only make one circuit modification per some reasonable period of time.

## Third iteration
The circuits for both player's paddles contains five wires, each with two full columns of Hadamard gates, and a column full of phase-rotation (Rz) gates in-between the Hadamard columns. During gameplay, each player rotates its Rz gates individually in pi/8 increments in such a way that the paddle collapses in a location that returns the ball. In fairness to the human player, the computer may only make one pi/8 rotation per some reasonable period of time to a gate.
