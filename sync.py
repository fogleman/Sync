from ctypes import *
import math
import random

WIDTH = 32
HEIGHT = 18
INFLUENCE = 0.0025
PERIOD = 2.0
SPEED = 1.0

def f(x):
    return 1 - math.e ** -x

def g(y):
    return math.log(1 / (1 - y)) if y < 1 else 50

class cModel(Structure):
    _fields_ = [
        ('width', c_int),
        ('height', c_int),
        ('threshold', c_double),
        ('influence', c_double),
        ('values', POINTER(c_double)),
    ]

dll = CDLL('_sync')
dll.update.argtypes = [POINTER(cModel), c_double]

class Model(object):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.count = self.width * self.height
        self.threshold = f(PERIOD)
        self.influence = INFLUENCE
        self.reset()
    def reset(self):
        self.sync = False
        self.model = cModel()
        self.model.width = self.width
        self.model.height = self.height
        self.model.threshold = self.threshold
        self.model.influence = self.influence
        self.model.values = (c_double * self.count)()
        for i in xrange(self.count):
            self.model.values[i] = random.random() * g(self.threshold)
    def update(self, dt):
        result = dll.update(byref(self.model), dt * SPEED)
        if result == self.count:
            self.sync = True
        return result
    def get_values(self):
        return [f(self.model.values[i]) / self.threshold
            for i in xrange(self.count)]
