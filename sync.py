from ctypes import *
import math
import random

WIDTH = 12
HEIGHT = 12
DEPTH = 12
INFLUENCE = 0.002
PERIOD = 3.0
SPEED = 1.0
SIMILARITY = 4

def f(x):
    return 1 - math.e ** -x

def g(y):
    return math.log(1 / (1 - y)) if y < 1 else 50

class cModel(Structure):
    _fields_ = [
        ('width', c_int),
        ('height', c_int),
        ('depth', c_int),
        ('threshold', c_double),
        ('influence', c_double),
        ('weights', POINTER(c_double)),
        ('values', POINTER(c_double)),
    ]

dll = CDLL('_sync')
dll.update.argtypes = [POINTER(cModel), c_double]

class Model(object):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.depth = DEPTH
        self.count = self.width * self.height * self.depth
        self.threshold = f(PERIOD)
        self.influence = INFLUENCE
        self.reset()
    def reset(self):
        self.sync = 0
        self.model = cModel()
        self.model.width = self.width
        self.model.height = self.height
        self.model.depth = self.depth
        self.model.threshold = self.threshold
        self.model.influence = self.influence
        self.model.weights = (c_double * self.count)()
        self.model.values = (c_double * self.count)()
        for i in xrange(self.count):
            self.model.weights[i] = (1.0 + random.random() / SIMILARITY -
                1.0 / (SIMILARITY * 2))
            self.model.values[i] = f(random.random() * g(self.threshold))
    def update(self, dt):
        result = dll.update(byref(self.model), dt * SPEED)
        self.sync = max(self.sync, result)
        return result
    def get_values(self):
        return [self.model.values[i] / self.threshold
            for i in xrange(self.count)]
