# Testing document

Both pathfinding algorithms are tested using unit tests with simple matrices. Additionally, their correctness is verified with Moving AI's scenario files for solved example routes. The algorithms are also compared against each other using 10 random start and end points on an existing Moving AI map (this is included in the [JPS unit testing file](https://github.com/gitjuli94/pathfinding/blob/main/src/tests/unittests/test_JPS.py "JPS unit testing file")).


## Unit testing

### Dijkstra

The Dijkstra algorithm is tested in this [file](https://github.com/gitjuli94/pathfinding/blob/main/src/tests/unittests/test_dijkstra.py "file") for:
- finding the shortest path in a small simple matrix
- finding the shortest path in two big complex matrices (from Moving AI scenarios)
- finding no path due to obstacles in the matrix
- finding no path with erroneous input
- testing the path reconstruction

Additionally, the network module utilized in the Dijkstra pathfinding algorithm is tested with unit tests to verify the creation of adjacency lists from simple input matrices. The unit tests can be found [here](https://github.com/gitjuli94/pathfinding/blob/main/src/tests/unittests/test_network.py "here").

### Jump point search

The Jump point search algorithm is tested in this [file](https://github.com/gitjuli94/pathfinding/blob/main/src/tests/unittests/test_JPS.py "file") for:
- finding the shortest path in two big complex matrices (from Moving AI scenarios)
- finding no path due to obstacles in the matrix
- finding no path with erroneous input
- testing the path reconstruction
- testing against Dijkstra with 10 random inputs in a big matrix (from Moving AI scenarios)

### Unit testing coverage report

The unit testing coverage report can be obtained using the following commands (frameworks coverage and pytest must be installed):

```bash
coverage run --branch -m pytest src
```

```bash
coverage report -m
```

![image](https://github.com/gitjuli94/pathfinding/blob/main/images/coverage_report.jpg)

## Performance testing

The algorithms are tested with 100 iterations with 3 different maps. The performance test can be run [here](https://github.com/gitjuli94/pathfinding/blob/main/src/tests/performance_test.py "here"). The start and end coordinates are selected from Moving AI scenario files for long routes. The scenario text files also saved in folder "util_files" and can be downloaded from [here](https://www.movingai.com/benchmarks/street/index.html "here").

- Test 1: map newyork_256
    - Coordinates: start:(4, 234), end: (243, 37) (y, x)
- Test 2: map paris_512
    - Coordinates: start:(491, 61), end: (7, 504) (y, x)
- Test 3: map sydney_1024
    - Coordinates: start:(8, 16), end: (993, 982) (y, x)

***Map: 256x256 New York***
| Algorithm           | Run time (avg 100 iterations)            |
| ------------------- | ---------------------------------------- |
| Dijkstra            | 0.195 seconds                            |
| Jump Point Search   | 0.028 seconds                            |

***Map: 512x512 Paris***
| Algorithm           | Run time (avg 100 iterations)            |
| ------------------- | ---------------------------------------- |
| Dijkstra            | 0.903 seconds                            |
| Jump Point Search   | 0.180 seconds                            |

***Map: 1024x1024 Sydney***

| Algorithm          | Run time (avg 100 iterations)            |
| ------------------ | ---------------------------------------- |
| Dijkstra           | 4.197 seconds                            |
| Jump Point Search  | 0.755 seconds                            |
