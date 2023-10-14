# Attacking-Pairs ♟️
The goal is to find a way to place 5 queen chess pieces in a way that none of them cross paths. Here, we experiment with 2 algorithms - genetic and hill-climbing.
This repository consists of 3 files:
- board.py = file that contains properties of a 5x5 chess board
- genetic.py = file that performs the genetic algorithm with 8 states, using selection, crossover, and mutation to find a solution
- hill.py = file that performs the hill-climbing algorithm to find a solution

## How to use: 💡
1. Pick which algorithm you would like to use to find a solution, either genetic or hill-climbing
2. After choosing, type one of these in the terminal:
    - python genetic.py
    - python hill.py
3. After execution, the chess board will be printed out with the solution