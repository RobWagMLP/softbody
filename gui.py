from tkinter import *
import tkinter as tk
from masspoint import MassPoint 
from soft_object import SoftObject
import vector
import math

root = tk.Tk()
canvas = tk.Canvas(root, width='800', height='800', bg='black')

line = 0
rad =10

#point_grid = [
#    [{"point": vector.obj(x=100, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, 
#     {"point": vector.obj(x=350, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}]
#    ]

point_grid = [
    [{"point": vector.obj(x=100, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=150, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=200, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=300, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=350, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=400, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}],
    [{"point": vector.obj(x=100, y = 150), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=150, y = 150), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=200, y = 150), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 150), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=300, y = 150), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=350, y = 150), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=400, y = 150), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}],
    [{"point": vector.obj(x=100, y = 200), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=150, y = 200), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=200, y = 200), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 200), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=300, y = 200), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=350, y = 200), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=400, y = 200), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}],
    [{"point": vector.obj(x=100, y = 250), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=150, y = 250), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=200, y = 250), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 250), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=300, y = 250), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=350, y = 250), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=400, y = 250), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}]
]

soft_object = None

def draw_grid():
    global point_grid, rad

    for i in range(0, len(point_grid) ):
        row = point_grid[i]
        for j in range (0, len(row) ):
            point = row[j]
            point["pId"] = canvas.create_oval(point["point"].x, point["point"].y, point["point"].x + rad*2,  point["point"].y + rad*2, fill='green', tags=("dots",))
            canvas.pack()
            if i > 0:
                ref_point = point_grid[i - 1][j]
                point["lIds"]["rO"] = canvas.create_line(point["point"].x + rad, point["point"].y + rad, ref_point["point"].x + rad,ref_point["point"].y + rad, fill='white', width='2', tags=("lines",))
                canvas.pack()
            if i > 0 and j < len(row) -1:
                ref_point = point_grid[i - 1][j + 1]
                point["lIds"]["rd"] = canvas.create_line(point["point"].x + rad, point["point"].y + rad, ref_point["point"].x + rad,ref_point["point"].y + rad, fill='white', width='2', tags=("lines",))
                canvas.pack()
            if j < len(row) -1:
                ref_point = point_grid[i][j + 1]
                point["lIds"]["rr"] = canvas.create_line(point["point"].x + rad, point["point"].y + rad, ref_point["point"].x + rad,ref_point["point"].y + rad, fill='white', width='2', tags=("lines",))
                canvas.pack()
            if j < len(row) -1 and i < len(point_grid) - 1:
                ref_point = point_grid[i + 1][j + 1]
                point["lIds"]["rU"] = canvas.create_line(point["point"].x + rad, point["point"].y + rad, ref_point["point"].x + rad,ref_point["point"].y + rad, fill='white', width='2', tags=("lines",))
                canvas.pack()
            row[j] = point
        point_grid[i] = row
        canvas.tag_lower("lines")

def length(vec: vector.VectorObject2D):
    return math.sqrt(vec.x*vec.x + vec.y*vec.y)

def mainLoop():
    object = soft_object.update_stats()

    for i in range(0, len(object) ):
        row = object[i]
        for j in range(0, len(row) ):
            mp = row[j]["mp"].pos
            canvas.moveto(point_grid[i][j]["pId"], mp.x, mp.y)
            if i > 0:
                ref_point = object[i - 1][j]["mp"].pos
                canvas.coords(point_grid[i][j]["lIds"]["rO"], mp.x + rad, mp.y + rad, ref_point.x + rad, ref_point.y + rad)
            if i > 0 and j < len(row) -1:
                ref_point = object[i - 1][j + 1]["mp"].pos
                canvas.coords(point_grid[i][j]["lIds"]["rd"], mp.x + rad, mp.y + rad, ref_point.x + rad, ref_point.y + rad)
            if j < len(row) -1:
                ref_point = object[i][j + 1]["mp"].pos
                canvas.coords(point_grid[i][j]["lIds"]["rr"], mp.x + rad, mp.y + rad, ref_point.x + rad, ref_point.y + rad)
            if j < len(row) -1 and i < len(point_grid) - 1:
                ref_point = object[i + 1][j + 1]["mp"].pos
                canvas.coords(point_grid[i][j]["lIds"]["rU"], mp.x + rad, mp.y + rad, ref_point.x + rad, ref_point.y + rad)
    root.after(int(1000/60), mainLoop )

def main():
    global point_grid, soft_object, rad

    draw_grid()
    soft_object = SoftObject(point_grid, 20, 50, rad, 5)
    root.after(100, mainLoop )
    root.mainloop()

main()