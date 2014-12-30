import wx
from functools import partial

class SegmentWidget(wx.Panel):
    FONT_WORD = None
    FONT_ROMAJI = None

    def __init__(self, word, romaji, definition, top_frame, *args, **kwargs):
        super(SegmentWidget, self).__init__(*args, **kwargs)
        if SegmentWidget.FONT_WORD is None:
            SegmentWidget.FONT_WORD = wx.Font(22, wx.ROMAN, wx.NORMAL, wx.NORMAL,
                                face='Yu Mincho')

        if SegmentWidget.FONT_ROMAJI is None:
            SegmentWidget.FONT_ROMAJI = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.NORMAL,
                                face='Times New Roman')

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self._romaji_label = wx.StaticText(self, label=romaji)
        self._romaji_label.SetFont(SegmentWidget.FONT_ROMAJI)
        self._romaji_label.SetForegroundColour((220,) * 3)
        self.bindToParent(self._romaji_label)
        self._romaji_label.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        vbox.Add(self._romaji_label, flag=wx.TOP)

        self._word_label = wx.StaticText(self, label=word)
        self._word_label.SetFont(SegmentWidget.FONT_WORD)
        self._word_label.SetForegroundColour((255,) * 3)
        self.bindToParent(self._word_label)
        self._word_label.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        vbox.Add(self._word_label, flag=wx.BOTTOM)

        self._definition = definition
        self._top_frame = top_frame

        self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
        self.Bind(wx.EVT_MOTION, self.onMouseEvent)
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))

        self.Fit()

        self._enter_cnt = 0
        self._clicked = False

    @staticmethod
    def bindToParent(label):
        label.Bind(wx.EVT_MOUSE_EVENTS, partial(SegmentWidget.postToParent, label))

    @staticmethod
    def postToParent(control, e):
        wx.PostEvent(control.GetParent(), e)

    def onMouseEvent(self, e):
        old_cnt = self._enter_cnt
        if e.Entering():
            self._enter_cnt += 1
        elif e.Leaving():
            self._enter_cnt -= 1
        elif e.LeftUp():
            self._top_frame.showHTML(self, self._definition)

        if self._enter_cnt > 0 and old_cnt <= 0:
            self.SetBackgroundColour((140, ) * 3)
            self.Refresh()
        elif self._enter_cnt <= 0 and old_cnt > 0:
            self.SetBackgroundColour(None)
            self.Refresh()

        e.Skip()

class PageConstructor(object):
    def __init__(self, frame, *args, **kwargs):
        super(PageConstructor, self).__init__(*args, **kwargs)
        self._frame = frame
        self._labels = []

    def generate(self, words):
        self.clear()
        for word, romaji, definition in words:
            self.generateOne(word, romaji, definition)
        self._frame.Layout()

    def generateOne(self, word, romaji, definition):
        label = SegmentWidget(word, romaji, definition, self._frame, self._frame)
        self._frame._hbox.Add(label)
        self._labels.append(label)

    def clear(self):
        for l in self._labels:
            self._frame._hbox.Remove(l)
            l.Destroy()
        self._labels = []
