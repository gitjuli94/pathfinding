import sys
from pathlib import Path
# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.JPS import JPS
from algorithms.dijkstra import Dijkstra
from data.performance_test_maps.newyork_256 import input_matrix as newyork_256
from data.performance_test_maps.paris_512 import input_matrix as paris_512
from data.performance_test_maps.sydney_1024 import input_matrix as sydney_1024

def perfomance_test(iterations, map, start, end):
    dijkstra_times = []
    jps_times = []

    for i in range(iterations):
        _, _, time = dijkstra.solve(start, end, map)
        dijkstra_times.append(time)

    d_avg = sum(dijkstra_times) / len(dijkstra_times)
    print(f"Dijkstra took on average: {d_avg} seconds")

    for i in range(iterations):
        _, _, time = jps.solve(start, end, map)
        jps_times.append(time)

    j_avg = sum(jps_times) / len(jps_times)
    print(f"JPS took on average: {j_avg} seconds")


if __name__ == "__main__":
    jps = JPS()
    dijkstra = Dijkstra()

    maps = [newyork_256, paris_512, sydney_1024]
    # 90	NewYork_1_256.map	256	256	26	250	226	5	361.11479034
    # 189	Paris_1_512.map	512	512	144	498	474	4	758.08744506
    # 364	Sydney_0_1024.map	1024	1024	0	1018	1022	106	1456.58405303
    coords = [[(250, 26), (5, 226)], # newyork
              [(498, 144), (4, 474)], # paris
              [(1018, 0), (106, 1022)]] # sydney
    iterations = 100

    for i, m in enumerate(maps):
        map = maps[i].input_matrix
        print("Starting test {i} with map {map}")
        print(f"Map size: {len(map)}x{len(map[0])}")
        print(f"Running {iterations} iterations")
        perfomance_test(iterations, map, coords[i][0], coords[i][1])
