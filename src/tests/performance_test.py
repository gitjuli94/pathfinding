import sys
from pathlib import Path
# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(src_dir))

from algorithms.JPS import JPS
from algorithms.dijkstra import Dijkstra
from data.performance_test_maps.newyork_256 import input_matrix as newyork_256
from data.performance_test_maps.paris_512 import input_matrix as paris_512
from data.performance_test_maps.sydney_1024 import input_matrix as sydney_1024
import time

def perfomance_test(n, map, start, end):
    dijkstra_record = []
    jps_record = []

    jps = JPS(map)
    dijkstra = Dijkstra(map)

    for i in range(n):
        start_time = time.time()
        result = dijkstra.find_distances(start, end)
        end_time = time.time()
        dijkstra_record.append(end_time - start_time)

    d_avg = round((sum(dijkstra_record) / len(dijkstra_record)), 3)
    print(f"Dijkstra average run time: {d_avg} seconds")

    for i in range(n):
        start_time = time.time()
        result = jps.jump_point_search(start, end)
        end_time = time.time()
        jps_record.append(end_time - start_time)

    j_avg = round((sum(jps_record) / len(jps_record)), 3)
    print(f"JPS average run time: {j_avg} seconds")


if __name__ == "__main__":

    maps = {
        "newyork_256": newyork_256,
        "paris_512": paris_512,
        "sydney_1024": sydney_1024
    }
    # routes from path scenarios from moving ai, text files also saved in folder: "util_files":

    # 86	NewYork_1_256.map	256	256	234	4	37	243	344.90158691
    # 182	Paris_1_512.map	512	512	61	491	504	7	728.56053314
    # 364	Sydney_0_1024.map	1024	1024	16	8	982	993	1457.76781920
    # ##364	Sydney_0_1024.map	1024	1024	0	1018	1022	106	1456.58405303

    coords = [[(4,234), (243,37)], # newyork
              [(491, 61), (7, 504)], # paris
              [(8,16), (993,982)]] # sydney
    n = 100

    for i, (name, matrix) in enumerate(maps.items()):
        print(f"Test {i+1} with map {name}")
        print(f"Coordinates: start:{coords[i][0]}, end: {coords[i][1]}")
        print(f"Map size: {len(matrix)}x{len(matrix[0])}")
        print(f"Running {n} times")
        perfomance_test(n, matrix, coords[i][0], coords[i][1])
        print()
