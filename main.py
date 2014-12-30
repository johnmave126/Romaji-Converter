#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
import MainView
import PageConstructor
import ClipboardWatcher
import MeCab
import pykakasi.kakasi as kakasi
import HJDictionary
from utils import callLater

class MainController(wx.App):
    def __init__(self, *args, **kwargs):
        super(MainController, self).__init__(*args, **kwargs)
        self._clipboard_watcher = ClipboardWatcher.ClipboardWatcher(self.onClipboardChange)
        self._clipboard_watcher.start()
        self._tagger = MeCab.Tagger('--node-format=%m\\t%f[8]\\n --eos-format= --unk-format=%m')

        kakasi_ = kakasi()
        kakasi_.setMode("H","a")
        kakasi_.setMode("K","a")
        kakasi_.setMode("J","a")
        kakasi_.setMode("r","Hepburn")
        kakasi_.setMode("C", True)
        kakasi_.setMode("c", False)

        self._converter = kakasi_.getConverter()

        self._dict = HJDictionary.HJDictionary()

    @callLater
    def onClipboardChange(self, value):
        # First transform value to UTF-8 whatever original encoding is
        if not isinstance(value, unicode):
            value = unicode(value, 'utf-8')

        # First feed value to mecab
        words = self._tagger.parse(value.encode('utf-8')).decode('utf-8').split('\n')
        words = map(lambda x: x.split('\t'), (w for w in words if len(w) > 0))
        words = map(lambda x: x if len(x) == 2 else x * 2, words)

        words, katana = map(lambda x: list(x), zip(*words))

        res = zip(words,
                    map(lambda x: self._converter.do(x), katana),
                    self._dict.lookup(words))

        self._pager.generate(res)

    def OnInit(self):
        self._frame = MainView.GalgameRomaji(None, -1, 'Galgamer')
        self.SetTopWindow(self._frame)

        self._frame.Bind(wx.EVT_CLOSE, self.OnClose)

        self._pager = PageConstructor.PageConstructor(self._frame)
        return True

    def OnClose(self, e):
        self._clipboard_watcher.stop()
        e.Skip()

app = MainController(0)
app.MainLoop()
