__author__ = 'Noah'

def draw(canvas):
    self.canvas.delete('all')
    self.canvas.create_text(100, 10, text='FPS: ' + str(1/deltat))
    self.draw_cube(5, 7, -1, 1, -1, 1)
    self.draw_cube(5, 7, 3, 1, -1, 1)