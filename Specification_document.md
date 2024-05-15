#Specification Document

##Topic
Pathfinding Algorithm: How to efficiently find the fastest/shortest route in a network between two points?

##Programming Language
The project will be implemented using Python. I am proficient in Python and Visual Basic.

##Data Structures and Algorithms
The project compares two different algorithms: Dijkstra and Jump Point Search (JPS). The program utilizes built-in data structures in Python, such as lists, sets, heaps, and dictionaries.

##Program Inputs
The program takes a pixel map as input. JPS operates in a two-dimensional grid, so the pixel map can be directly used as input. However, Dijkstra's algorithm understands nodes and their connecting edges, so the pixel map is converted into a network representation before the algorithm execution.

##Time and Space Complexities
The Dijkstra algorithm's time complexity is O(n + m log m). The O(n) time complexity arises from traversing the nodes in the network, while the O(m log m) complexity originates from inserting each edge into a heap and subsequently removing it. The space complexity is O(n) or O(n+m), depending on how dense the network is. 

The JPS algorithm significantly reduces the number of nodes explored due to pruning large areas of the search space. However, the time complexity depends on factors such as the amount of obstacles and possible simple routes between start and goal points. According to the graph being searched, the best case can have the time complexity of O(n) the worst case O(b^d),  where b refers to the branching factor and 'd' represents the depth of the search.

The JPS algorithm needs a linear amount of space so its space complexity is O(n).

##Core of the Assignment
The core of the work lies in the pathfinding algorithms and their comparison. The purpose of the work is to create two algorithms that find the shortest route on a pixel map from point A to point B.

##Study Program
Tietojenkäsittelytieteen kandidaatti (TKT) (BSc in Computer Science)

##Documentation Language
The documentation of the project is written in English (except for the weekly reports).

##References
University of Helsinki. Data Structures and Algorithms course. Visited 15.5.2024
[https://tira.mooc.fi/kevat-2024/osa14/#dijkstran-algoritmi
](https://tira.mooc.fi/kevat-2024/osa14/#dijkstran-algoritmi
)

ICAPS 2014: Daniel Harabor on "Improving Jump Point Search". 
[https://www.youtube.com/watch?v=NmM4pv8uQwI](https://www.youtube.com/watch?v=NmM4pv8uQwI)









