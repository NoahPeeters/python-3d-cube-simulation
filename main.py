__author__ = 'Noah'

from engine import Engine
import tkinter as tk
import time
import math
import os
import pickle

rot_speed = 0.1
canvas_width = 800
canvas_height = 400
render_dist = 6


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.e = Engine(self.canvas, canvas_width, canvas_height)
        self.e.update_position(0, 2, 0, 0, 0)
        self.speed_up = self.speed_right = self.speed_forward = self.alpha = self.beta = 0
        self.accel_right = self.accel_forward = 0
        self.block_x = self.block_z = self.block_y = 0
        self.target_block_x = self.target_block_y = self.target_block_z = 0
        self.block_state = 0
        self.block_dist = 3
        self.block_dist_speed = self.block_dist_accel = 0
        self.jumped = self.block_marked = False
        self.mouse_start_x = self.mouse_start_y = 0
        self.root.focus_set()
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.root.bind("<Button-1>", self.mouse_down)
        self.root.bind("<B1-Motion>", self.mouse_moved)

        self.load()

        self.last_time = time.time()
        self.update_clock()
        self.root.mainloop()

    def load(self):
        if os.path.isfile('save.p'):
            data = pickle.load(open("save.p", "rb"))
            self.e.world = data[0]
            self.e.x = data[1]
            self.e.y = data[2]
            self.e.z = data[3]
            self.e.alpha = data[4]
            self.e.beta = data[5]
            self.block_marked = data[6]
            self.block_x = data[7]
            self.block_y = data[8]
            self.block_z = data[9]
            self.block_state = data[10]
            self.block_dist = data[11]

    def save(self):
        data = [self.e.world, self.e.x, self.e.y, self.e.z, self.e.alpha, self.e.beta, self.block_marked, self.block_x,
                self.block_y, self.block_z, self.block_state, self.block_dist]
        pickle.dump(data, open("save.p", "wb"))

    def update_clock(self):
        delta_t = time.time() - self.last_time
        self.last_time = time.time()

        self.block_marked = False
        if self.block_state == 0:
            for i in range(5):
                x = self.e.x + self.e.player_wx * i
                y = self.e.y + self.e.player_wy * i
                z = self.e.z + self.e.player_wz * i
                if self.e.block_exists(x, y, z):
                    self.block_marked = True
                    self.target_block_x = round(x)
                    self.target_block_y = round(y)
                    self.target_block_z = round(z)
                    break

        if self.block_state == 1:
            self.target_block_x = self.e.x + self.e.player_wx * self.block_dist
            self.target_block_y = self.e.y + self.e.player_wy * self.block_dist
            self.target_block_z = self.e.z + self.e.player_wz * self.block_dist
        elif self.block_state == 2:
            self.target_block_x = round(self.block_x)
            self.target_block_y = round(self.block_y)
            self.target_block_z = round(self.block_z)
            self.block_state = 3

        new_block_x = self.block_x + (self.target_block_x - self.block_x) / 2 * delta_t * 15
        new_block_y = self.block_y + (self.target_block_y - self.block_y) / 2 * delta_t * 15
        new_block_z = self.block_z + (self.target_block_z - self.block_z) / 2 * delta_t * 15

        if not (
                    self.e.block_exists(new_block_x + 0.5, self.block_y, self.block_z) or self.e.block_exists(
                        new_block_x - 0.5,
                        self.block_y,
                        self.block_z)):
            self.block_x = new_block_x
        else:
            self.block_x = round(new_block_x)

        if not (self.e.block_exists(self.block_x, new_block_y + 0.5, self.block_z) or self.e.block_exists(self.block_x,
                                                                                                          new_block_y - 0.5,
                                                                                                          self.block_z)):
            self.block_y = new_block_y
        else:
            self.block_y = round(new_block_y)

        if not (self.e.block_exists(self.block_x, self.block_y, new_block_z + 0.5) or self.e.block_exists(self.block_x,
                                                                                                          self.block_y,
                                                                                                          new_block_z - 0.5)):
            self.block_z = new_block_z
        else:
            self.block_z = round(new_block_z)

        if self.block_state == 3:
            if abs(self.block_x - self.target_block_x) < 0.005 and abs(
                            self.block_y - self.target_block_y) < 0.005 and abs(
                        self.block_z - self.target_block_z) < 0.005:
                self.block_state = 0
                key = self.e.get_key(self.target_block_x, self.target_block_y, self.target_block_z)
                self.e.world[key] = 1

        self.block_dist_speed = self.block_dist_speed + self.block_dist_accel * delta_t - self.block_dist_speed / 6

        self.block_dist += self.block_dist_speed * delta_t
        self.speed_forward = self.speed_forward + self.accel_forward * delta_t - self.speed_forward / 3
        self.speed_right = self.speed_right + self.accel_right * delta_t - self.speed_right / 3
        self.e.move(delta_t * self.speed_forward, delta_t * self.speed_up,
                    delta_t * self.speed_right)

        if self.speed_up <= 0 and self.e.block_exists(self.e.x, self.e.y - 1.50000001, self.e.z):
            self.speed_up = 0
            self.e.y = round(self.e.y)
        else:
            self.speed_up -= 9.81 * delta_t

        self.e.rotate(delta_t * rot_speed * self.alpha, delta_t * rot_speed * self.beta)
        self.alpha = 0
        self.beta = 0
        self.canvas.delete('all')
        self.render()
        self.canvas.create_text(90, 10, text='FPS: ' + str(int(1 / delta_t)))
        # self.canvas.create_text(90, 25, text='x: ' + str(self.e.x))
        # self.canvas.create_text(90, 40, text='y: ' + str(self.e.y))
        # self.canvas.create_text(90, 55, text='z: ' + str(self.e.z))
        # self.canvas.create_text(90, 70, text='a: ' + str(self.e.alpha))
        # self.canvas.create_text(90, 85, text='b: ' + str(self.e.beta))
        self.root.after(1, self.update_clock)

    @staticmethod
    def get_key(x, y, z):
        return str(x) + '/' + str(y) + '/' + str(z)

    def render(self):
        all_sites = []
        for x in range(int(self.e.x - render_dist), int(self.e.x + render_dist + 1)):
            for y in range(int(self.e.y - render_dist - 10), int(self.e.y + render_dist + 1)):
                for z in range(int(self.e.z - render_dist), int(self.e.z + render_dist + 1)):
                    a = -math.atan2(self.e.x - x, self.e.z - z) - math.pi / 2
                    dx = self.e.x - x
                    dz = self.e.z - z
                    if abs(self.e.alpha - a) < math.pi / 3 or \
                                    abs(self.e.alpha - a - math.pi * 2) < math.pi / 3 or \
                                    math.sqrt(dx * dx + dz * dz) < 2:
                        block_id = self.e.get_block(x, y, z)
                        if block_id != 0:
                            if self.block_marked and x == self.target_block_x and y == self.target_block_y and z == self.target_block_z:
                                block_id = -1
                            for i in self.get_sites(x, y, z, block_id):
                                all_sites.append(i)
        if self.block_state != 0:
            for i in self.get_sites(self.block_x, self.block_y, self.block_z, -2, True):
                all_sites.append(i)
        for l, c, block_id in reversed(sorted(all_sites, key=lambda info: info[0])):
            color = self.e.get_color(block_id)
            self.e.draw_poly(c, color, 'black')

    def get_sites(self, x, y, z, block_id, get_all=False):
        x1 = x - 0.5
        x2 = x + 0.5
        y1 = y - 0.5
        y2 = y + 0.5
        z1 = z - 0.5
        z2 = z + 0.5

        all_sites = []

        if get_all or not self.e.block_exists(x + 1, y, z):
            all_sites.append([math.sqrt((x + 0.5 - self.e.x) ** 2 + (y - self.e.y) ** 2 + (z - self.e.z) ** 2),
                              [[x2, y1, z1], [x2, y2, z1], [x2, y2, z2], [x2, y1, z2]], block_id])
        if get_all or not self.e.block_exists(x - 1, y, z):
            all_sites.append([math.sqrt((x - 0.5 - self.e.x) ** 2 + (y - self.e.y) ** 2 + (z - self.e.z) ** 2),
                              [[x1, y1, z1], [x1, y2, z1], [x1, y2, z2], [x1, y1, z2]], block_id])

        if get_all or not self.e.block_exists(x, y + 1, z):
            all_sites.append([math.sqrt((x - self.e.x) ** 2 + (y + 0.5 - self.e.y) ** 2 + (z - self.e.z) ** 2),
                              [[x1, y2, z1], [x2, y2, z1], [x2, y2, z2], [x1, y2, z2]], block_id])
        if get_all or not self.e.block_exists(x, y - 1, z):
            all_sites.append([math.sqrt((x - self.e.x) ** 2 + (y - 0.5 - self.e.y) ** 2 + (z - self.e.z) ** 2),
                              [[x1, y1, z1], [x2, y1, z1], [x2, y1, z2], [x1, y1, z2]], block_id])

        if get_all or not self.e.block_exists(x, y, z + 1):
            all_sites.append([math.sqrt((x - self.e.x) ** 2 + (y - self.e.y) ** 2 + (z + 0.5 - self.e.z) ** 2),
                              [[x1, y1, z2], [x2, y1, z2], [x2, y2, z2], [x1, y2, z2]], block_id])
        if get_all or not self.e.block_exists(x, y, z - 1):
            all_sites.append([math.sqrt((x - self.e.x) ** 2 + (y - self.e.y) ** 2 + (z - 0.5 - self.e.z) ** 2),
                              [[x1, y1, z1], [x2, y1, z1], [x2, y2, z1], [x1, y2, z1]], block_id])
        return all_sites

    def mouse_down(self, event):
        self.mouse_start_x = event.x
        self.mouse_start_y = event.y

    def mouse_moved(self, event):
        self.alpha -= event.x - self.mouse_start_x
        self.beta -= event.y - self.mouse_start_y
        self.mouse_start_x = event.x
        self.mouse_start_y = event.y

    def key_down(self, event):
        if event.char == 'w':
            self.accel_forward = 25
        elif event.char == 's':
            self.accel_forward = -25
        elif event.char == 'd':
            self.accel_right = 25
        elif event.char == 'a':
            self.accel_right = -25
        elif event.char == 'o':
            self.block_dist_accel = 40
        elif event.char == 'l':
            self.block_dist_accel = -40
        elif event.char == 'b':
            if self.block_state == 1:
                self.block_state = 2
            elif self.block_marked:
                self.block_x = self.target_block_x
                self.block_y = self.target_block_y
                self.block_z = self.target_block_z
                self.block_state = 1
                key = self.e.get_key(self.target_block_x, self.target_block_y, self.target_block_z)
                self.e.world[key] = 0
                self.block_dist = math.sqrt(
                    (self.target_block_x - self.e.x) ** 2 + (self.target_block_y - self.e.y) ** 2 + (
                        self.target_block_z - 0.5 - self.e.z) ** 2)
        elif event.char == 'n' and self.block_state == 0:
            self.block_x = self.e.x
            self.block_y = self.e.y + 2
            self.block_z = self.e.z
            self.block_state = 1
        elif event.char == 'u':
            self.save()
        elif event.char == ' ':
            if self.speed_up == 0:
                self.speed_up = 5

    def key_up(self, event):
        if event.char in 'ws':
            self.accel_forward = 0
        elif event.char in 'ad':
            self.accel_right = 0
        elif event.char in 'lo':
            self.block_dist_accel = 0


app = App()
