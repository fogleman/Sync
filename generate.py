import sync
import time
import wx

FPS = 20
WIDTH = 16
HEIGHT = 16
SPEED = 1.0
PERIOD = 3.0
INFLUENCE = 0.0028
SIMILARITY = 0

def generate_image(model):
    data = []
    w, h = model.width, model.height
    values = model.get_values()
    for y in xrange(h):
        for x in xrange(w):
            i = y * w + x
            v = int(values[i] * 255)
            v = min(v, 255)
            v = 255 - v * 3 if v < 85 else 0
            r, g, b = v / 2, v, v / 4
            data.append(chr(r) + chr(g) + chr(b))
    data = ''.join(data)
    image = wx.EmptyImage(w, h)
    image.SetData(data)
    return image

def main():
    app = wx.App()
    model = sync.Model(WIDTH, HEIGHT, 1, SPEED, PERIOD, INFLUENCE, SIMILARITY)
    for i in range(FPS * 120):
        print i
        model.update(1.0 / FPS)
        image = generate_image(model)
        image.SaveFile('frames/%06d.png' % i, wx.BITMAP_TYPE_PNG)

if __name__ == '__main__':
    main()
