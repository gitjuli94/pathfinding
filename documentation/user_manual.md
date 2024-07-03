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
python3 main.py
```

6) **Run the algorithms**

Run the algorithms in the GUI using the buttons described below. Use the buttons sequentially from top to bottom. Additionally, pay attention to any notifications that might appear in the terminal.

![image](https://github.com/gitjuli94/pathfinding/blob/main/images/buttons.jpg)

* **Start**: Click to select the start node within the white area on the map.
* **End**: Click to select the end node within the white area on the map.
* **Maps dropdown**: Select a map to load from the available options.
* **Load Map**: Load the selected map before running.
* **Run JPS**: Run the Jump Point Search algorithm, visualize the path, and print the results.
* **Run Dijkstra**: Run the Dijkstra algorithm, visualize the path, and print the results.

### Running the tests

1) **Ensure the virtual environment "poetry" is running**
```bash
poetry shell
```
2) **Run the unit tests**
```bash
coverage run --branch -m pytest src
```
3) **Show the coverage report**
```bash
coverage report -m
```
