import sync
import time
import wx

class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent)
        self.model = sync.Model()
        self.timestamp = time.time()
        self.brushes = [wx.Brush(wx.Colour(0, x / 2, x)) for x in range(256)]
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
        dc.SetBackground(wx.BLACK_BRUSH)
        dc.Clear()
        dc.SetPen(wx.TRANSPARENT_PEN)
        p = 0
        n = self.model.size
        cw, ch = self.GetClientSize()
        w, h = cw / n, ch / n
        values = self.model.get_values()
        for y in xrange(n):
            for x in xrange(n):
                i = y * n + x
                v = int(values[i] * 255)
                v = min(v, 255)
                dc.SetBrush(self.brushes[v])
                dc.DrawRectangle(x * w, y * h, w - p, h - p)
    def on_update(self):
        now = time.time()
        dt = now - self.timestamp
        self.timestamp = now
        self.model.update(dt * 2)
        if self.model.sync:
            self.model.reset()
        self.Refresh()
        wx.CallLater(10, self.on_update)

def main():
    app = wx.App(False)
    frame = wx.Frame(None)
    Panel(frame)
    frame.SetTitle('Sync')
    frame.SetClientSize((512, 512))
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
