import sync
import time
import wx

class Panel(wx.Panel):
    def __init__(self, parent, model):
        super(Panel, self).__init__(parent)
        self.model = model
        self.timestamp = time.time()
        self.brushes = [wx.Brush(wx.Colour(x / 2, x, x / 4))
            for x in range(256)]
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.on_update()
    def on_size(self, event):
        event.Skip()
        self.Refresh()
    def on_left_down(self, event):
        self.model.reset()
        self.Refresh()
    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        self.draw(dc)
    def draw(self, dc):
        dc.SetBackground(wx.BLACK_BRUSH)
        dc.Clear()
        dc.SetPen(wx.TRANSPARENT_PEN)
        p = 8
        mw, mh = self.model.width, self.model.height
        cw, ch = self.GetClientSize()
        w, h = cw / mw, ch / mh
        dx, dy = (cw - w * mw) / 2 + p / 2, (ch - h * mh) / 2 + p / 2
        values = self.model.get_values()
        for y in xrange(mh):
            for x in xrange(mw):
                i = y * mw + x
                v = int(values[i] * 255)
                v = min(v, 255)
                v = 255 - v * 3 if v < 85 else 0
                dc.SetBrush(self.brushes[v])
                dc.DrawRectangle(x * w + dx, y * h + dy, w - p, h - p)
    def create_bitmap(self):
        cw, ch = self.GetClientSize()
        bitmap = wx.EmptyBitmap(cw, ch)
        dc = wx.MemoryDC(bitmap)
        self.draw(dc)
        return bitmap
    def on_update(self):
        now = time.time()
        dt = now - self.timestamp
        self.timestamp = now
        self.model.update(dt * 1)
        if self.model.sync == self.model.count:
            self.model.reset()
        self.Refresh()
        wx.CallLater(10, self.on_update)

def main():
    app = wx.App(False)
    frame = wx.Frame(None)
    model = sync.Model()
    Panel(frame, model)
    frame.SetTitle('Sync')
    frame.SetClientSize((model.width * 24, model.height * 24))
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
