from tkinter import *
import tkinter as tk
from masspoint import MassPoint 
from soft_object import SoftObject
import vector
import math

root = tk.Tk()
canvas = tk.Canvas(root, width='800', height='800', bg='black')

line = 0
rad =5

#point_grid = [
#    [{"point": vector.obj(x=100, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, 
#     {"point": vector.obj(x=150, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}]
#    ]

point_grid = [
    [{"point": vector.obj(x=100, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=130, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=160, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=190, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=220, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=280, y = 100), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}],
    [{"point": vector.obj(x=100, y = 130), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=130, y = 130), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=160, y = 130), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=190, y = 130), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=220, y = 130), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 130), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=280, y = 130), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}],
    [{"point": vector.obj(x=100, y = 160), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=130, y = 160), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=160, y = 160), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=190, y = 160), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=220, y = 160), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 160), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=280, y = 160), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}],
    [{"point": vector.obj(x=100, y = 190), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=130, y = 190), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=160, y = 190), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=190, y = 190), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=220, y = 190), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=250, y = 190), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}, {"point": vector.obj(x=280, y = 190), "pId": 0, "lIds": {"rO": 0, "rd": 0, "rr": 0, "rU": 0}}]
]

line_a_diag = vector.obj(x=0 ,  y=400)
line_b_diag = vector.obj(x=200, y=600)

line_a_hor = vector.obj(x=0   , y=800)
line_b_hor = vector.obj(x=2000, y=800)

soft_object = None

def draw_grid():
    global point_grid, rad

    for i in range(0, len(point_grid) ):
        row = point_grid[i]
        for j in range (0, len(row) ):
            point = row[j]
            point["pId"] = canvas.create_oval(point["point"].x -rad , point["point"].y - rad, point["point"].x + rad,  point["point"].y + rad, fill='green', tags=("dots",))
            canvas.pack()
            if i > 0:
                ref_point = point_grid[i - 1][j]
                point["lIds"]["rO"] = canvas.create_line(point["point"].x , point["point"].y, ref_point["point"].x,ref_point["point"].y, fill='white', width='2', tags=("lines",))
                canvas.pack()
            if i > 0 and j < len(row) -1:
                ref_point = point_grid[i - 1][j + 1]
                point["lIds"]["rd"] = canvas.create_line(point["point"].x , point["point"].y, ref_point["point"].x,ref_point["point"].y, fill='white', width='2', tags=("lines",))
                canvas.pack()
            if j < len(row) -1:
                ref_point = point_grid[i][j + 1]
                point["lIds"]["rr"] = canvas.create_line(point["point"].x , point["point"].y, ref_point["point"].x,ref_point["point"].y, fill='white', width='2', tags=("lines",))
                canvas.pack()
            if j < len(row) -1 and i < len(point_grid) - 1:
                ref_point = point_grid[i + 1][j + 1]
                point["lIds"]["rU"] = canvas.create_line(point["point"].x, point["point"].y, ref_point["point"].x,ref_point["point"].y, fill='white', width='2', tags=("lines",))
                canvas.pack()
            row[j] = point
        point_grid[i] = row

        canvas.create_line(line_a_diag.x, line_a_diag.y    , line_b_diag.x, line_b_diag.y   , width='3', tags=("lines",), fill="white")
        canvas.create_line(line_a_hor.x , line_a_hor.y + 3 , line_b_hor.x , line_b_hor.y + 3, width='3', tags=("lines",), fill="white")
        canvas.pack
        canvas.tag_lower("lines")

def length(vec: vector.VectorObject2D):
    return math.sqrt(vec.x*vec.x + vec.y*vec.y)

def mainLoop():
    global line_a_diag, line_b_diag, line_a_hor, line_b_hor

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
    root.after(1, mainLoop )

def main():
    global point_grid, soft_object, rad, line_a_diag, line_b_diag, line_a_hor, line_b_hor

    draw_grid()
    soft_object = SoftObject(point_grid, 15000, 30, rad, 2, [[line_a_diag, line_b_diag], [line_a_hor, line_b_hor]])
    root.after(500, mainLoop )
    root.mainloop()

main()