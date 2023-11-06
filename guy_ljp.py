from tkinter import *
import tkinter as tk
from masspoint import MassPoint 
from ljp import LJP
import vector

root = tk.Tk()
canvas = tk.Canvas(root, width='800', height='800', bg='black')
particle_ids = []
line = 0
rad = 3

line_a_diag = vector.obj(x=0 ,  y=500)
line_b_diag = vector.obj(x=2000, y=500)

line_a_hor = vector.obj(x=0   , y=800)
line_b_hor = vector.obj(x=2000, y=800)

cloud = 0

def draw_grid(particles):
    global line_a_diag, line_b_diag, line_a_hor, line_b_hor, canvas

    canvas.create_line(line_a_diag.x, line_a_diag.y    , line_b_diag.x, line_b_diag.y   , width='3', tags=("lines",), fill="white")
    canvas.create_line(line_a_hor.x , line_a_hor.y + 3 , line_b_hor.x , line_b_hor.y + 3, width='3', tags=("lines",), fill="white")
    for particle in particles:
        particle_ids.append(canvas.create_oval(particle.pos.x - rad, particle.pos.y - rad, particle.pos.x + rad, particle.pos.y + rad, fill='green', tag=("particle",)))

    canvas.tag_raise("particle")
    canvas.tag_lower("lines")
    canvas.pack()
    

def mainLoop():
    global line_a_diag, line_b_diag, line_a_hor, line_b_hor, cloud

    particles = cloud.calc_frame()
    for i in range(0, len(particles)):
        particle = particles[i]
        canvas.moveto(particle_ids[i], particle.pos.x - rad, particle.pos.y - rad)
    canvas.pack()
    root.after(1, mainLoop )

def main():
    global rad, line_a_diag, line_b_diag, line_a_hor, line_b_hor, cloud

    cloud = LJP(2, 5, 4., 5. + rad, rad, 8, 4, [[line_a_diag, line_b_diag]])

    draw_grid(cloud.particles)
    
    root.after(5000, mainLoop )
    root.mainloop()

main()