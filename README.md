# QPong
A quantum version of classic game Pong using qikist and pygame. This is a project for the Qiskit Camp 2019 made by Huang Junye, Jarrod Reilly, Anastasia Jeffery and James Weaver based on James Weaver's quantum-circuit-pygame package: https://github.com/JavaFXpert/quantum-circuit-pygame

## Description
Using the Qiskit and Pygame frameworks, create a Pong game in which a human competes against the computer. Each player's "paddle" is realized by a quantum circuit that results in a state vector in a superposition. When the ball gets close to a player's paddle area, the quantum state is measured, collapsing to a basis state that determines the paddle's location.

## Installation
To play the game, you will need to install Python and a few required packages. To do that, you need to use command line tool (Command Prompt for Windows or Terminal for macOS).

### Open command line tool

On Windows, open Command Prompt by typing "Command Prompt" on the search box of Start menu. Check this link if you are not sure about how to do that: https://www.wikihow.com/Open-the-Command-Prompt-in-Windows

On macOS, press Command + Space to open Spotlight. Type "Terminal" on Spotlight to open Terminal. Check this link if you are not sure about how to do that: https://www.wikihow.com/Open-a-Terminal-Window-in-Mac

### Install Python
You can install Python from https://www.python.org/ or install Anaconda from https://www.anaconda.com

### Install required packages
There are three Python packages required to run the game: Pygame, qiskit and matplotlib.

Run `pip install [package name]` on command line tool (same for Windows and macOS) to install the packages. For example:
```console
pip install pygame
```
### Install QPong

Clone or download the master branch by clicking the green button on the top right corner on this page (above the files and below "contributors"). Unzip the files to the "Downloads" folder on your computer.

Change the directory to the downloaded files. (Downloads/QPong-master)

On Windows, run the following code to change your directory to the QPong folder:
```console
cd C:\users\[your username]\downloads\QPong-master\
```
On macOS, run the following code to change your directory to the QPong folder:
```console
cd Downloads/QPong-master/
```

On both Windows and macOS, run the following command to start the game: 
```console
python main.py
```

## How to play

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
