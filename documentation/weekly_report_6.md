# Weekly report 6

1. This week I fixed the JPS algorithm to list the jump points correctly and to print them in the GUI. We revised the project with the guiding professor and checked the heuristics (they were correct in the end, octile distance was used). Turns out my JPS algorithm was slower than Dijkstra with big maps. I compared to the example algorithm that I had used as a model for my project, and tested directly with it how long it takes to solve the same map. It solved it as slow as mine, so the example wasn't a good choise to follow in this project. After this discovery, I have been rebuilding the JPS with a completely different approach, using a simple adjacency list for the nodes instead of the more complex graph object that was utilized in the example JPS algorithm. I also added in the GUI the visualization of the visited nodes.

In addition, I peer reviewed a project about data compressing, which was a very interesting topic to me.

I used aprox. 21 hours this week on the project.

2. The JPS is now under construction again. Now it seems to find the same paths as my dijkstra, and it works faster tha dijkstra. The unit tests for jps have to be rewritten because the algorithm was completely changed.

3. I understood the heuristics better for this topic after the meeting. I learned about other approaches on the JPS algorithm and compared different projects on it. I learned that I should have been comparing the run times between the algorithms with larger maps way earlier. I understood the importance of data structures in run times - the graph object (used in the JPS i had built) was way too complex compared to a simple neighbor dictionary. The simpler the better...

4. My rhetorical question is whether my project will be ready for the demonstration after this week's setback :D

5. I have to finish the new JPS and its tests and implement them again in the GUI for the demonstration. I also have to finish the documentation.
