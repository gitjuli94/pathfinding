"""
A graphical user interface to test and visualize the algorithms.
"""

import importlib
import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk
from tkinter import messagebox


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from algorithms.JPS import jps  # Adjust the import based on your function
#from algorithms.dijkstra import dijkstra  # Adjust the import based on your function

# Function to draw the grid and path
def draw_grid(canvas, path):
    canvas.delete("all")
    for (x, y) in path:
        canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill="blue")

class PathFindingApp:
    def __init__(self, root):
        self.cell_size = 6

        self.root = root
        self.root.title("Path Finding Algorithms")
        self.map = None
        self.start_coord = None
        self.end_coord = None

        # Create input fields and buttons
        input_frame = tk.Frame(root)
        input_frame.pack(side=tk.LEFT)

        self.start_label = tk.Label(input_frame, text="Start (x, y):")
        self.start_label.grid(row=0, column=0)
        self.start_entry = tk.Entry(input_frame, width=5)
        self.start_entry.grid(row=0, column=1)

        self.end_label = tk.Label(input_frame, text="End (x, y):")
        self.end_label.grid(row=1, column=0)
        self.end_entry = tk.Entry(input_frame, width=5)
        self.end_entry.grid(row=1, column=1)

        self.map_options = tk.StringVar()
        self.map_options.set("milan")  # Default map option

        map_menu = tk.OptionMenu(input_frame, self.map_options, "Milan", "Shanghai", "NewYork")
        map_menu.grid(row=2, column=0)

        self.load_map_button = tk.Button(input_frame, text="Load Map", command=self.load_map)
        self.load_map_button.grid(row=3, column=0)

        self.run_jps_button = tk.Button(input_frame, text="Run JPS", command=self.run_jps)
        self.run_jps_button.grid(row=4, column=0)

        self.run_dijkstra_button = tk.Button(input_frame, text="Run Dijkstra", command=self.run_dijkstra)
        self.run_dijkstra_button.grid(row=5, column=0)

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        #Load default map
        self.load_map()

    def on_canvas_click(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        if self.start_coord is None:
            self.start_coord = (row, col)
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, f"{col}, {row}")
        elif self.end_coord is None:
            self.end_coord = (row, col)
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, f"{col}, {row}")

    def load_map(self):
        map_name = self.map_options.get()
        # Load a map here
        try:
            map_module = importlib.import_module(f'data.maps.{map_name.lower()}')
            self.map = np.array(map_module.input_matrix)
            #print(self.map)
            messagebox.showinfo("Map Loaded")
            self.draw_map()
        except ImportError as e:
            messagebox.showerror("Error", f"Failed to load map: {e}")

    def draw_map(self):
        if self.map is None:
            messagebox.showerror("Error")
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

    def run_jps(self):
        pass
        """start = tuple(map(int, self.start_entry.get().split(',')))
        end = tuple(map(int, self.end_entry.get().split(',')))
        path = jps(self.map, start, end, 25, self.map.flatten())
        draw_grid(self.canvas, path)"""

    def run_dijkstra(self):
        pass
        """start = tuple(map(int, self.start_entry.get().split(',')))
        end = tuple(map(int, self.end_entry.get().split(',')))
        path = dijkstra(self.map, start, end, 25, self.map.flatten())
        draw_grid(self.canvas, path)"""

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = PathFindingApp(root)
    app.load_map()
    root.mainloop()
