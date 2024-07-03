# Implementation document

This document describes the implementation details of the project for path finding algorithms. It provides information about how the path finding application is designed and executed with the chosen algorithms.

## Project overview

The project centers around comparing two distinct pathfinding algorithms: Dijkstra and JPS (Jump Point Search). It involves the development of a locally deployable application capable of executing both algorithms, visualizing the resulting routes, and displaying relevant metrics. Users have the flexibility to select the starting and ending points on a pixel map within the application interface.

## Technologies used

### Programming language

The project is programmed with Python.

### Dependency management

Dependency management is implemented using Poetry.

### Frameworks and libraries

The application is built using Tkinter for the GUI. Other frameworks and libraries used in the project are:
* NumPy
* Poetry
* Heapq
* Math
* Time
* Random

### Development tools

The version control of the project is done with Git and the project's repository is in GitHub.

### Deployment platforms

The application can be deployed locally using Tkinter as the GUI library.

## Algorithms and data structures

Two different existing algorithms are implemented within the project: Dijkstra and JPS. Data structures are lists, dictionaries, tuples, heaps and sets.

### Path finding algorithms

Both pathfinding algorithms determine the shortest route between the start and end nodes. The distance is measured in pixels, and diagonal movement behind corners is not allowed; corners must be passed orthogonally.

#### Dijkstra

Dijkstra's algorithm expands a parent node and calculates the shortest known distance from the start to its neighboring nodes. These nodes are stored in a priority queue (min-heap) based on their distance, and new neighbors are processed according to their priority in the queue.

More about Dijkstra in this [Wikipedia article](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm "Wikipedia article")

#### Jump Point Search

The JPS is a pathfinding algorithm that uses pruned neighbor rules to determine the search direction of nodes and identifies jump points based on the position of forced neighbors. Forced neighbors are nodes that must be considered due to the presence of obstacles adjacent to them.

The algorithm extends jump points through iterative computation, selecting the least costly node among the candidate jump points for the subsequent path. These points are stored in a priorityqueue (min-heap), similar to Dijkstra algorithm.

The cost of each jump point is a heuristic estimation of the remaining distance from the jump point to the end node. In this project, the octile distance is used for heuristics.

The use of jump points significantly reduces the number of processed nodes and the runtime compared to Dijkstra, making JPS more efficient in many scenarios.

More about JPS in this [(article)](https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf "(article)").

### Helper functions

#### Network

The Network module creates an adjacency list for the nodes in the input matrix, which is used by the Dijkstra algorithm. It adds edges for all available nodes in eight directions, excluding those that would move diagonally past an obstacle, thereby forcing the path to go orthogonally around corners.

## Coding standards
The tools and methodologies used to ensure code quality, including testing and code coverage, are:
* Pylint
* Pytest
* Coverage

## Use of AI

Large Language Models (LLM's) weren't used for code generation in the path finding algorithms. Chat-GPT was utilized to assist in creating code for the GUI, since it wasn't a crucial part of the project and it was a new area for me.

Chat-GPT was also employed to identify performance and precision issues in the jump point search algorithm and it was quite useful for that purpose. Still, it didn't create the solution for the precision issues (it didn't offer any solutions that would fix the issue). But it gave ideas what was possible to improve in the code.

Chat-GPT was also utilized to summarize new topics when I was doing the peer reviews of other projects. It helped to grasp new concepts quickly and provided clear overviews, making the review process more efficient.

## Summary, conclusion

Both algorithms seem to find the shortest path. The JPS is more efficient especially with big maps where start and end node are selected in a way that the octile heuristic approximation is the most accurate.

## References

https://tira.mooc.fi/kevat-2024/osa14/

https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

https://encyclopedia.pub/entry/24246

https://blog.finxter.com/jump-search-algorithm-in-python-a-helpful-guide-with-video/

https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf
