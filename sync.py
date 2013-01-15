from ctypes import *
import math
import random

SIZE = 32
INFLUENCE = 0.003

def f(x):
    return 1 - math.e ** -x

def g(y):
    return math.log(1 / (1 - y)) if y < 1 else 50

class cModel(Structure):
    _fields_ = [
        ('size', c_int),
        ('threshold', c_double),
        ('influence', c_double),
        ('values', POINTER(c_double)),
    ]

dll = CDLL('_sync')
dll.update.argtypes = [POINTER(cModel), c_double]

class Model(object):
    def __init__(self):
        self.size = SIZE
        self.count = self.size * self.size
        self.threshold = f(2)
        self.influence = INFLUENCE
        self.reset()
    def reset(self):
        self.model = cModel()
        self.model.size = self.size
        self.model.threshold = self.threshold
        self.model.influence = self.influence
        self.model.values = (c_double * self.count)()
        for i in xrange(self.count):
            self.model.values[i] = random.random() * g(self.threshold)
    def update(self, dt):
        dll.update(byref(self.model), dt)
    def get_values(self):
        return [f(self.model.values[i]) / self.threshold
            for i in xrange(self.count)]
