# Simulations

A collection of interactive physics, cellular automata, procedural generation, and artificial life simulations built using Python, Pygame, NumPy, and Matplotlib.

## Included Simulations

* __ParticlePlayground.py:__ A physics particle playground sandbox featuring elements like sand, water, stone, and acid with dissolution rules.
* __GameOfLife.py:__ Conway's classic cellular automata simulation.
* __langtonsAnt.py:__ A cellular automata simulation tracking an ant navigating a grid based on simple color-flip rules.
* __Flocking.py:__ A Boids flocking simulation demonstrating alignment, cohesion, and separation behaviors among agents.
* __evolution.py:__ Gooblet evolution agent simulation where entities monitor thirst levels, expand their search radius, and seek out water sources.
* __2dWorldGen.py:__ Interactive 2D procedural world and terrain generator driven by Perlin noise.
* __Bakterien.py:__ A mathematical and animated graphical simulation tracking bacterial population growth, nutrition depletion, and decline over time.

## Prerequisites and Installation

To run these simulations, you will need Python installed along with the required libraries.

1. Clone the repository:
   git clone https://github.com/txtrm/simulations
   cd simulations

2. Install dependencies:
   pip install pygame numpy perlin-noise matplotlib

## How to Run

Execute any script individually using Python from your terminal:

python ParticlePlayground.py
python GameOfLife.py
python Flocking.py
