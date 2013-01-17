from ctypes import *
import math
import random

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
    def __init__(
        self, width, height, depth, speed, period, influence, similarity):
        self.width = width
        self.height = height
        self.depth = depth
        self.count = self.width * self.height * self.depth
        self.speed = speed
        self.threshold = f(period)
        self.influence = influence
        self.similarity = similarity
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
            self.model.weights[i] = (1.0 + random.random() / self.similarity -
                1.0 / (self.similarity * 2))
            self.model.values[i] = f(random.random() * g(self.threshold))
    def update(self, dt):
        result = dll.update(byref(self.model), dt * self.speed)
        self.sync = max(self.sync, result)
        return result
    def get_values(self):
        return [self.model.values[i] / self.threshold
            for i in xrange(self.count)]
