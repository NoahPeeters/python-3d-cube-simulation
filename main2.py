__author__ = 'Noah'

from engine import Engine
import tkinter as tk
import time
#import world

speed = 1
rot_speed = 1
zoom = 500
canvas_width = 800
canvas_height = 400


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.e = Engine()
        self.e.update_position(0, 0, 0, 0, 0, 0)
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.speed_up = self.speed_right = self.speed_forward = self.speed_alpha = self.speed_beta = self.speed_gamma = 0
        self.root.focus_set()
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.last_time = time.time()
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        deltat = time.time() - self.last_time
        self.last_time = time.time()
        self.e.move(deltat * speed * self.speed_forward, deltat * speed * self.speed_up, deltat * speed * self.speed_right)
        self.e.rotate(deltat * rot_speed * self.speed_alpha, deltat * rot_speed * self.speed_beta, deltat * rot_speed * self.speed_gamma)
        self.canvas.delete('all')
        self.canvas.create_text(30, 10, text='FPS: ' + str(int(1/deltat)))
        self.draw_cube(2, 5, -0.5, 0.5, -0.5, 0.5, 'red')
        self.draw_cube(3.45, 3.55, 0.5, 0.6, -0.05, 0.05, 'red')
        self.draw_poly([[2, -0.5, -0.5], [2, -0.5, 0.5], [5, -0.5, 0.5], [5, -0.5, -0.5]], 'red')
        #self.draw_cube(5, 7, 3, 1, -1, 1)
        #world.draw(self.canvas)
        self.root.after(1, self.update_clock)

    def draw_poly(self, p, color=None):
        allCoords = []
        for i in p:
            a = self.e.get_2d_point(*i)

            allCoords.append(self.screen_pos_x(a[0]))
            allCoords.append(self.screen_pos_y(a[1]))
        if color:
            self.canvas.create_polygon(*allCoords, fill=color)
        else:
            self.canvas.create_polygon(*allCoords)

    def draw_cube(self, x1, x2, y1, y2, z1, z2, color=None):
        self.draw_poly([[x1, y1, z1], [x2, y1, z1], [x2, y2, z1], [x1, y2, z1]], color)
        self.draw_poly([[x1, y1, z2], [x2, y1, z2], [x2, y2, z2], [x1, y2, z2]], color)

        self.draw_poly([[x1, y2, z2], [x2, y2, z2], [x2, y2, z1], [x1, y2, z1]], color)
        self.draw_poly([[x1, y2, z2], [x2, y2, z2], [x2, y2, z2], [x1, y2, z2]], color)

        # self.draw_line([x1, y1, z1], [x2, y1, z1])
        # self.draw_line([x1, y1, z1], [x1, y2, z1])
        # self.draw_line([x1, y1, z1], [x1, y1, z2])
        #
        # self.draw_line([x2, y2, z1], [x1, y2, z1])
        # self.draw_line([x2, y2, z1], [x2, y1, z1])
        # self.draw_line([x2, y2, z1], [x2, y2, z2])
        #
        # self.draw_line([x2, y1, z2], [x1, y1, z2])
        # self.draw_line([x2, y1, z2], [x2, y2, z2])
        # self.draw_line([x2, y1, z2], [x2, y1, z1])
        #
        # self.draw_line([x1, y2, z2], [x2, y2, z2])
        # self.draw_line([x1, y2, z2], [x1, y1, z2])
        # self.draw_line([x1, y2, z2], [x1, y2, z1])

    def draw_line(self, start3, end3):
        start2 = self.e.get_2d_point(start3[0], start3[1], start3[2])
        end2 = self.e.get_2d_point(end3[0], end3[1], end3[2])
        self.canvas.create_line(self.screen_pos_x(start2[0]), self.screen_pos_y(start2[1]), self.screen_pos_x(end2[0]),  self.screen_pos_y(end2[1]), fill="#476042")

    def screen_pos_x(self, x):
        return x*zoom+canvas_width/2

    def screen_pos_y(self, x):
        return x*zoom+canvas_height/2

    def key_down(self, event):
        if event.keycode == 852087:
            self.speed_forward = 1
        elif event.keycode == 65651:
            self.speed_forward = -1
        elif event.keycode == 131172:
            self.speed_right = 1
        elif event.keycode == 97:
            self.speed_right = -1
        elif event.keycode == 131074:
            self.speed_up = 1
        elif event.keycode == 3211296:
            self.speed_up = -1
        elif event.keycode == 5636148:
            self.speed_alpha = 1
        elif event.keycode == 5767222:
            self.speed_alpha = -1
        elif event.keycode == 5505074:
            self.speed_beta = -1
        elif event.keycode == 5963832:
            self.speed_beta = 1
        elif event.keycode == 5832759:
            self.speed_gamma = 1
        elif event.keycode == 6029369:
            self.speed_gamma = -1
        elif event.char == 'j':
            self.speed_alpha = 1
        elif event.char == 'l':
            self.speed_alpha = -1
        elif event.char == 'k':
            self.speed_beta = 1
        elif event.char == 'i':
            self.speed_beta = -1

    def key_up(self, event):
        if event.keycode in [852087, 65651]:
            self.speed_forward = 0
        elif event.keycode in [131172, 97]:
            self.speed_right = 0
        elif event.keycode in [131074, 3211296]:
            self.speed_up = 0
        elif event.keycode in [5636148, 5767222]:
            self.speed_alpha = 0
        elif event.keycode in [5963832, 5505074]:
            self.speed_beta = 0
        elif event.keycode in [5832759, 6029369]:
            self.speed_gamma = 0
        elif event.char in ['j', 'l']:
            self.speed_alpha = 0
        elif event.char in ['i', 'k']:
            self.speed_beta = 0

        print(event.keycode)


app=App()