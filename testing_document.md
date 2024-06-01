# Testing document

## Unit testing

### Dijkstra
The Dijkstra algorithm is tested for:
- finding a path in a simple matrix
- finding no path with erroneous input
- finding no path due to obstacles in the matrix
- testing the path reconstruction

### JPS
No testing created yet.

## Testing coverage report
(pathfinding-poetry-py3.12) juliarahkonen@Julia-MacBook-Pro pathfinding % coverage report -m

Name                         Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------
src/algorithms/JPS.py          123    123     62      0     0%   4-247
src/algorithms/dijkstra.py      63     16     22      3    73%   55, 66-67, 79-97
src/algorithms/graph.py        150    150     72      0     0%   6-197
src/algorithms/network.py       22      0     10      0   100%
src/algorithms/random.py        56     56     26      0     0%   1-85
------------------------------------------------------------------------
TOTAL                          414    345    192      3    16%
