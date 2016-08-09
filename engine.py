__author__ = 'Noah'

import math


class Engine:
    def __init__(self, canvas, width, height):
        self.x = self.y = self.z = 0
        self.alpha = self.beta = 0
        self.zoom = 500
        self.canvas = canvas
        self.canvas_width = width
        self.canvas_height = height
        self.player_wx = self.player_wy = self.player_wz = 0
        self.world = {}
        self.cos_alpha = self.sin_alpha = self.cos_beta = self.sin_beta = 0

    def update_position(self, x, y, z, alpha, beta):
        self.x = x
        self.y = y
        self.z = z
        self.alpha = alpha
        self.beta = beta
        self.calculate_angle_functions()

    @staticmethod
    def generate(x, y, z):
        if round(math.sin(x / 6) + math.sin(z / 6) * 3) >= y >= -10:
            return 1
        return 0

    def get_block(self, x, y, z):
        key = self.get_key(x, y, z)
        if key not in self.world:
            self.world[key] = self.generate(x, y, z)
        return self.world[key]

    def block_exists(self, x, y, z):
        return self.get_block(round(x), round(y), round(z)) > 0

    def move(self, steps_x, steps_y, steps_z):
        cx = steps_x * self.cos_alpha - steps_z * self.sin_alpha
        cz = steps_x * self.sin_alpha + steps_z * self.cos_alpha

        new_x = self.x + cx
        self.y += steps_y
        new_z = self.z + cz

        if not (self.block_exists(new_x, self.y, self.z) or self.block_exists(new_x, self.y - 1.4, self.z)):
            self.x = new_x
        if not (self.block_exists(self.x, self.y, new_z) or self.block_exists(self.x, self.y - 1.4, new_z)):
            self.z = new_z

    def rotate(self, alpha, beta):
        self.beta = min(max(self.beta + beta, -math.pi / 2), math.pi / 2)
        self.alpha = (self.alpha - alpha) % (2 * math.pi)

        self.calculate_angle_functions()

        cx_m = 1
        cy_m = 0
        cz_m = 0

        cx_r1 = cx_m * self.cos_beta - cy_m * self.sin_beta
        cy_r1 = cx_m * self.sin_beta + cy_m * self.cos_beta
        cz_r1 = cz_m

        self.player_wx = cx_r1 * math.cos(-self.alpha) + cz_r1 * math.sin(-self.alpha)
        self.player_wy = cy_r1
        self.player_wz = -cx_r1 * math.sin(-self.alpha) + cz_r1 * math.cos(-self.alpha)

    def calculate_angle_functions(self):
        self.cos_alpha = math.cos(self.alpha)
        self.sin_alpha = math.sin(self.alpha)
        self.cos_beta = math.cos(self.beta)
        self.sin_beta = math.sin(self.beta)

    @staticmethod
    def get_key(x, y, z):
        return str(x) + '/' + str(y) + '/' + str(z)

    def get_2d_point(self, x, y, z):
        cx_m = (x - self.x)
        cy_m = -(y - self.y)
        cz_m = (z - self.z)

        cx_r1 = cx_m * self.cos_alpha + cz_m * self.sin_alpha
        cy_r1 = cy_m
        cz_r1 = -cx_m * self.sin_alpha + cz_m * self.cos_alpha

        cx = cx_r1 * self.cos_beta - cy_r1 * self.sin_beta
        cy = cx_r1 * self.sin_beta + cy_r1 * self.cos_beta
        cz = cz_r1

        visible = True

        if cx <= 0:
            cz *= (-cx / 100 + 1)
            cy *= (-cx / 100 + 1)
            cx = 0.000001
            visible = False

        return self.screen_pos_x(cz / cx), self.screen_pos_y(cy / cx), visible

    @staticmethod
    def get_color(block_id):
        if block_id == 1:
            return 'red'
        elif block_id == -1:
            return 'blue'
        elif block_id == -2:
            return 'blue'

    def draw_poly(self, p, color='', outline=''):
        all_coords = []
        visible = False
        for i in p:
            a = self.get_2d_point(i[0], i[1], i[2])

            all_coords.append(a[0])
            all_coords.append(a[1])
            visible = visible or a[2]
        if visible:
            self.canvas.create_polygon(*all_coords, fill=color, outline=outline)

    def screen_pos_x(self, x):
        return x * self.zoom + self.canvas_width / 2

    def screen_pos_y(self, y):
        return y * self.zoom + self.canvas_height / 2
