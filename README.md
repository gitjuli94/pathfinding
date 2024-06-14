# Pathfinding
Comparison between two path finding algorthms Dijkstra and JPS (Jump Point Search).

## Maps
**Note: For week 4's peer review, only simple maps are included in the app, not the final maps**

Maps downloaded from the [MovingAI Benchmarks](https://www.movingai.com/benchmarks/street/index.html "Moving AI Lab Map Benchmarks") and modified into arrays with "1" and "0", the first being obstacle and the latter being free space. The conversion was done with a [python script](https://github.com/gitjuli94/pathfinding/blob/main/additional_scripts/maptolist.py "python script").

## Pathfinding Algorithms GUI
This application provides a graphical user interface (GUI) to test and visualize different pathfinding algorithms, including Dijkstra and Jump Point Search (JPS). The GUI is built using Tkinter which is a standard Python GUI library.

### Prerequisities
Before running the application, ensure that you have the following installed:

* Python 3.10 or higher
* Poetry for dependency management

### How to run the application
This guide is intended for macOS, for other OS's instructions might vary.


1) **Clone the repository**

```bash
git clone https://github.com/gitjuli94/pathfinding.git
```
2) **Go to the directory**

```bash
cd pathfinding
```

3) **Install dependencies**
```bash
poetry install
```

4) **Activate the virtual environment**
```bash
poetry shell
```

5) **Run the app**
```bash
python main.py
```

6) **Run the algorithms**

Run the algorithms in the GUI using the buttons explained below. Also, pay attention to possible notifications in the terminal.

* Start Button: Click to select the start pixel on the map.
* End Button: Click to select the end pixel on the map.
* Map Options Dropdown: Select a map to load from the available options.
* Load Map Button: Load the selected map for visualization.
* Run JPS Button: Run the Jump Point Search algorithm and visualize the path.
* Run Dijkstra Button: Run the Dijkstra algorithm and visualize the path.

![image](https://github.com/gitjuli94/pathfinding/assets/149376454/d0eabff3-da24-452f-b908-927fd9467f7a)

![image](https://github.com/gitjuli94/pathfinding/assets/149376454/2ebbd07b-e50b-4e2c-b36e-30d4b3a1e134)

