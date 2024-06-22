"""
A graphical user interface to test and visualize the algorithms.
Built using Tkinter which is a standard Python GUI library.
"""

import importlib

import numpy as np
from algorithms.dijkstra import Dijkstra
import algorithms.JPS as JPS

import time

import tkinter as tk
from tkinter import messagebox
from tkinter import *

class PathFindingApp:
    def __init__(self, root):

        self.cell_size = 7

        self.root = root
        self.root.title("Path Finding Algorithms")
        self.map = None

        self.start_coord = None
        self.end_coord = None
        self.selecting_start = False
        self.selecting_end = False

        #Create input fields and buttons
        input_frame = tk.Frame(root)
        input_frame.grid(row=0, column=0, sticky='NS')

        #buttons for interface
        self.start_button = tk.Button(input_frame, text="Start", command=self.click_start)
        self.start_button.grid(row=0, column=0, sticky = 'WE', padx=4)

        self.end_button = tk.Button(input_frame, text="End", command=self.click_end, state=tk.DISABLED)
        self.end_button.grid(row=1, column=0, sticky = 'WE', padx=4)

        self.map_options = tk.StringVar()
        self.map_options.set("Milan")  # Default map option

        map_menu = tk.OptionMenu(input_frame, self.map_options, "NewYork", "Shanghai", "Milan")
        map_menu.grid(row=2, column=0, sticky = 'WE', padx=4)

        self.load_map_button = tk.Button(input_frame, text="Load Map", command=self.load_map)
        self.load_map_button.grid(row=3, column=0, sticky = 'WE', padx=4)

        self.run_jps_button = tk.Button(input_frame, text="Run JPS", command=self.run_jps)
        self.run_jps_button.grid(row=4, column=0, sticky = 'WE', padx=4)

        self.run_dijkstra_button = tk.Button(input_frame, text="Run Dijkstra", command=self.run_dijkstra)
        self.run_dijkstra_button.grid(row=5, column=0, sticky = 'WE', padx=4)

        #create labels
        input_labels = tk.Frame(root)
        input_labels.grid(row=1, column=0, sticky='NS')

        self.label_empty = tk.Label(input_labels, text=" ", font=("Helvetica", 16))
        self.label_empty.grid(row=5, column=0, columnspan=2, sticky='NW', padx=4)

        self.label_n = tk.Label(input_labels, text="", font=("Helvetica", 16, "bold"))
        self.label_n.grid(row=1, column=0, columnspan=2, sticky='NW', padx=10)

        self.label0 = tk.Label(input_labels, text="", font=("Helvetica", 16))
        self.label0.grid(row=2, column=0, columnspan=2, sticky='NW', padx=4)

        self.label1 = tk.Label(input_labels, text="", font=("Helvetica", 16))
        self.label1.grid(row=3, column=0, columnspan=2, sticky='NW', padx=4)

        self.label2 = tk.Label(input_labels, text="", font=("Helvetica", 16))
        self.label2.grid(row=4, column=0, columnspan=2, sticky='NW', padx=4)

        self.label3 = tk.Label(input_labels, text="", font=("Helvetica", 16, "bold"))
        self.label3.grid(row=6, column=0, columnspan=2, sticky='NW', padx=10)

        self.label4 = tk.Label(input_labels, text="", font=("Helvetica", 16))
        self.label4.grid(row=7, column=0, columnspan=2, sticky='NW', padx=4)

        self.label5 = tk.Label(input_labels, text="", font=("Helvetica", 16))
        self.label5.grid(row=8, column=0, columnspan=2, sticky='NW', padx=4)

        self.label6 = tk.Label(input_labels, text="", font=("Helvetica", 16))
        self.label6.grid(row=9, column=0, columnspan=2, sticky='NW', padx=4)

        #map visualization configuration
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.grid(row=0, column=3, rowspan=16, sticky = 'NE', padx=4)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def click_start(self):
        self.selecting_start = True
        self.selecting_end = False
        self.end_button.config(state=tk.NORMAL)


    def click_end(self):

        self.selecting_start = False
        self.selecting_end = True
        self.end_button.config(state=tk.DISABLED)

    def on_canvas_click(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size

        self.coord = (row, col)
        x0 = col * self.cell_size
        y0 = row * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size


        if self.selecting_start:
            if self.map[row][col] == 0:
                self.end_coord = None
                if self.start_coord is not None: #reset previous to white
                    self.draw_map()

                self.start_coord = self.coord
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                print("start: ", self.start_coord)
                self.selecting_start = False
            else:
                print("out of free zone")

        if self.selecting_end:
            if self.map[row][col] == 0:
                if self.end_coord is not None: #reset previous to white
                    return

                self.end_coord = self.coord
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                print("end: ", self.end_coord)
                self.selecting_end = False
            else:
                print("out of free zone")



    def load_map(self):
        #empty the labels
        self.label_n.config(text="")
        self.label0.config(text="")
        self.label1.config(text="")
        self.label2.config(text="")
        self.label3.config(text="")
        self.label4.config(text="")
        self.label5.config(text="")
        self.label6.config(text="")

        #empty the previous input
        self.start_coord = None
        self.end_coord = None

        map_name = self.map_options.get()
        # Load a map here
        try:
            map_module = importlib.import_module(f'data.maps.{map_name.lower()}')
            self.matrix = map_module.input_matrix
            self.map = np.array(map_module.input_matrix)
            print("map loaded")
            #messagebox.showinfo("Map Loaded")
            self.draw_map()
        except ImportError as e:
            print("noi")
            messagebox.showerror("Error", f"Failed to load map: {e}")

    def draw_map(self):
        if self.map is None:
            #messagebox.showerror("Error")
            return

        self.canvas.delete("all")
        map_height = len(self.map)
        map_width = len(self.map[0])

        canvas_width = map_width * self.cell_size
        canvas_height = map_height * self.cell_size

        self.canvas.config(width=canvas_width, height=canvas_height)

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                color = "black" if self.map[i][j] == 1 else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_route(self, route, color):

        for node in route:
            if node != self.start_coord and node != self.end_coord:
                x0 = node[1] * self.cell_size
                y0 = node[0] * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_visited(self, visited, color, dot_radius=2):

        for node in visited:

            x_center = node[1] * self.cell_size + self.cell_size // 2
            y_center = node[0] * self.cell_size + self.cell_size // 2
            x0 = x_center - dot_radius
            y0 = y_center - dot_radius
            x1 = x_center + dot_radius
            y1 = y_center + dot_radius
            self.canvas.create_oval(x0, y0, x1, y1, outline=color, fill=color)


    def run_jps(self):

        start = self.start_coord
        end = self.end_coord
        neighbor_list, start_position, end_position, cols, field_status = \
            JPS.initialize_graph(self.map, start, end)
        #graph = JPS.initialize_graph(self.map, start, end)

        #measure path finding time
        start_time = time.time()
        result = JPS.jump_point_search(neighbor_list, start_position, end_position, cols, field_status)
        end_time = time.time()
       # print(result)

        if result:
            print(end_time - start_time)

            jpoints = result["jpoints"]
            absolute_distance = round(result["absolute_distance"], 1)
            visited = result["visited"]
            came_from = result["came_from"]
            end = result["end"]
            width = result["width"]
            full_path = JPS.reconstruct_full_path(came_from, end, width)

            self.label3.config(text=f"JPS:")
            self.label4.config(text=f"{round((end_time - start_time), 6):.6f} s")
            self.label5.config(text=f"distance: {absolute_distance}")
            self.label6.config(text=f"visited: {len(visited)}")
            self.draw_visited(visited.keys(), color="orange", dot_radius=2)
            self.draw_route(full_path, color="greenyellow")
            self.draw_route(jpoints, color="red")


           # print("full_path tässä", full_path)
           # print("visited", visited)
           # print("jpoints", jpoints)
        else:
            self.label4.config(text=f"No path found with JPS.")
            print("No path found.")

    def run_dijkstra(self):

        dijkstra = Dijkstra(self.map)
        start = self.start_coord
        end = self.end_coord

        #measure path finding time
        start_time = time.time()
        result = dijkstra.find_distances(start, end)
        end_time = time.time()

        if result:
            #routes = len(result["Routes"])
            shortest_path = result["shortestPath"]
            absolute_distance = round(result["absoluteDistance"], 1)
            visited = result["visited"]
            self.label_n.config(text=f"Dijkstra:")
            self.label0.config(text=f"{round((end_time - start_time), 6):.6f} s")
            self.label1.config(text=f"distance: {absolute_distance}")
            self.label2.config(text=f"visited: {len(visited)}")
            self.draw_visited(visited, color="seashell4")
            self.draw_route(shortest_path, color="deeppink")

        else:
            self.label1.config(text=f"No path found with Dijkstra.")
            print("No path found.")



# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    app = PathFindingApp(root)
    app.load_map()
    root.mainloop()


