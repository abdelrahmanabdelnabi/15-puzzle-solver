# N-puzzle solver

A solver for the 15-puzzle game (or any NxN puzzle).

The search agents implemented are DFS, BFS, and A* (with two different heuristic functions).

For a 3x3 puzzle (8-puzzle), the solver takes around 10 seconds to explore 180,000 states which is the number of states reachable from any initial state in a 3x3 puzzle.

TODO:
- Implement the simple algorithm to check if an NxN puzzle is solvable or not.
- Improve front-end experience, and input validation
- Improve the `decrease_key()` method in the heap. It is currently O(n).
- refactor the heap frontier implementation.

The frontend code was adopted from [Arnis Ritiņ](https://github.com/arnisritins/15-Puzzle) and modified to fit the solver.