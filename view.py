from pyglet.gl import *
from pyglet.window import key
import math
import random
import sync

def get_color(n):
    return (n / 2, n / 1, n / 4)

def cube_vertices(x, y, z, n):
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n, # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n, # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n, # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n, # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n, # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n, # back
    ]

class Model(object):
    def __init__(self):
        self.model = sync.Model()
        self.batch = pyglet.graphics.Batch()
        self.vertex_lists = {}
        for z in xrange(self.model.depth):
            for y in xrange(self.model.height):
                for x in xrange(self.model.width):
                    self.add_point((x, y, z))
    def add_point(self, position):
        if position in self.vertex_lists:
            return
        m = 1
        x, y, z = position
        x -= self.model.width / 2
        y -= self.model.height / 2
        z -= self.model.depth / 2
        x += random.random() / m - 1.0 / (m * 2)
        y += random.random() / m - 1.0 / (m * 2)
        z += random.random() / m - 1.0 / (m * 2)
        vertex_data = cube_vertices(x, y, z, 0.05)
        self.vertex_lists[position] = self.batch.add(len(vertex_data) / 3, 
            GL_QUADS, None,
            ('v3f', vertex_data),
            ('c3B', get_color(255) * 24))
    def reset(self):
        self.model.reset()
    def update(self, dt):
        self.model.update(dt)
        values = self.model.get_values()
        for z in xrange(self.model.depth):
            for y in xrange(self.model.height):
                for x in xrange(self.model.width):
                    i = (z * self.model.width * self.model.height +
                        y * self.model.width + x)
                    v = int(values[i] * 255)
                    v = min(v, 255)
                    v = 255 - v * 3 if v < 85 else 0
                    self.vertex_lists[(x, y, z)].colors = get_color(v) * 24

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.exclusive = False
        self.strafe = [0, 0]
        self.position = (0, 0, 0)
        self.rotation = (0, 0)
        self.reticle = None
        self.model = Model()
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18, 
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top', 
            color=(255, 255, 255, 255))
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)
    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive
    def get_sight_vector(self):
        x, y = self.rotation
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)
    def get_motion_vector(self):
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            m = math.cos(math.radians(y))
            dy = math.sin(math.radians(y))
            if self.strafe[1]:
                dy = 0.0
                m = 1
            if self.strafe[0] > 0:
                dy *= -1
            dx = math.cos(math.radians(x + strafe)) * m
            dz = math.sin(math.radians(x + strafe)) * m
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)
    def update(self, dt):
        speed = 4
        d = dt * speed
        dx, dy, dz = self.get_motion_vector()
        dx, dy, dz = dx * d, dy * d, dz * d
        x, y, z = self.position
        x, y, z = x + dx, y + dy, z + dz
        self.position = (x, y, z)
        self.model.update(dt)
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass
    def on_mouse_press(self, x, y, button, modifiers):
        if self.exclusive:
            self.model.reset()
        else:
            self.set_exclusive_mouse(True)
    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            m = 0.5
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)
    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
    def on_resize(self, width, height):
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width / 2, self.height / 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )
    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def set_3d(self):
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 100000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)
    def on_draw(self):
        self.clear()
        self.set_3d()
        self.model.batch.draw()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()
    def draw_label(self):
        x, y, z = self.position
        self.label.text = '%02d (%.2f, %.2f, %.2f)' % (
            pyglet.clock.get_fps(), x, y, z)
        self.label.draw()
    def draw_reticle(self):
        glColor3d(1, 1, 1)
        self.reticle.draw(GL_LINES)

def setup():
    glClearColor(0, 0, 0, 1)
    glEnable(GL_CULL_FACE)

def main():
    window = Window(width=800, height=600, caption='Sync', resizable=True)
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
